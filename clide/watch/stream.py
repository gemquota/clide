import json
import os
import time
import glob
import re
import threading
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add project root to sys.path for absolute imports
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from clide.kernel.loader import load_commands
from clide.brain.reason import classify_intent
from clide.watch.terminal import get_new_commands
from clide.brain.memory import get_embedding, search_registry
from clide.kernel import storage as db_manager
from clide.kernel.settings import load_config

config = load_config()
STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")
RECENT_MESSAGES_FILE = os.path.join(os.path.dirname(__file__), "recent_messages.json")
RECENT_MESSAGES_LIMIT = config["extraction"]["repetition_limit"]
GEMINI_TMP_DIR = os.environ.get("GEMINI_TMP_DIR") or "/data/data/com.termux/files/home/.gemini/tmp"
PID_FILE = os.path.join(os.path.dirname(__file__), "monitor.pid")

def load_recent_messages():
    if os.path.exists(RECENT_MESSAGES_FILE):
        try:
            with open(RECENT_MESSAGES_FILE, "r") as f:
                return json.load(f)
        except: pass
    return []

def save_recent_messages(messages):
    with open(RECENT_MESSAGES_FILE, "w") as f:
        json.dump(messages[-RECENT_MESSAGES_LIMIT:], f)

def detect_repetition(current_text, recent_messages):
    if not current_text or len(current_text) < 15: return False
    current_keywords = set(re.findall(r'\w{4,}', current_text.lower()))
    if not current_keywords: return False
    match_count = 0
    for msg in recent_messages:
        prev_keywords = set(re.findall(r'\w{4,}', msg.lower()))
        overlap = current_keywords.intersection(prev_keywords)
        if len(overlap) >= (len(current_keywords) * 0.5):
            match_count += 1
    return match_count >= 2

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
                if "session_trackers" not in state: state["session_trackers"] = {}
                return state
        except: pass
    return {"last_message_id": -1, "last_session_id": None, "session_trackers": {}, "usage_stats": {}, "last_shell_count": 0}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

class GeminiLogHandler(FileSystemEventHandler):
    def __init__(self, extractor):
        self.extractor = extractor
        self.last_process_time = {}

    def on_modified(self, event):
        if event.is_directory: return
        if event.src_path.endswith("logs.json"):
            now = time.time()
            if now - self.last_process_time.get(event.src_path, 0) < 2: return
            self.last_process_time[event.src_path] = now
            self.extractor.process_log_file(event.src_path)

class ClideExtractor:
    def __init__(self):
        db_manager.ensure_db()
        self.state = load_state()
        self.recent_messages = load_recent_messages()
        self.lock = threading.Lock()

    def process_log_file(self, log_path):
        with self.lock:
            try:
                with open(log_path, "r") as f:
                    logs = json.load(f)
                if not logs: return
                session_id = logs[0].get("sessionId")
                if not session_id: return
                last_id = self.state["session_trackers"].get(session_id, -1)
                new_messages = [m for m in logs if m["type"] == "user" and m["messageId"] > last_id]
                if new_messages:
                    print(f"\n[Monitor] Processing {len(new_messages)} new messages from {session_id[:8]}")
                    existing_cmds = load_commands()
                    for msg in new_messages:
                        text = msg['message']
                        if detect_repetition(text, self.recent_messages):
                            analysis = classify_intent(f"Automate this repetitive task: {text}", existing_cmds)
                        else:
                            analysis = classify_intent(text, existing_cmds)
                        embedding = get_embedding(text)
                        from clide.kernel.engine import handle_analysis
                        handle_analysis(analysis, msg, embedding)
                        self.recent_messages.append(text)
                        save_recent_messages(self.recent_messages)
                        last_id = msg["messageId"]
                    self.state["session_trackers"][session_id] = last_id
                    save_state(self.state)
            except Exception as e:
                print(f"[Error] Failed to process {log_path}: {e}")

    def poll_shell(self):
        while True:
            try:
                last_shell_count = self.state.get("last_shell_count", 0)
                new_shell_cmds, total_count = get_new_commands(last_shell_count)
                if new_shell_cmds:
                    from clide.brain.reason import classify_shell_intent
                    analysis = classify_shell_intent(new_shell_cmds)
                    if analysis and analysis.get("category") == "NEW_COMMAND":
                        db_manager.save_knowledge("NEW_COMMAND", analysis.get("raw_logic", ""), " && ".join(new_shell_cmds), importance=6, session_id="shell_session", msg_id=total_count, reasoning=analysis.get("reasoning"))
                    self.state["last_shell_count"] = total_count
                    save_state(self.state)
            except Exception as e:
                print(f"[Error] Shell poll failed: {e}")
            time.sleep(30)

    def run(self):
        print("CLIDE v0.7.0 (Watchdog Core) Active.")
        with open(PID_FILE, "w") as f: f.write(str(os.getpid()))
        observer = Observer()
        handler = GeminiLogHandler(self)
        observer.schedule(handler, GEMINI_TMP_DIR, recursive=True)
        observer.start()
        shell_thread = threading.Thread(target=self.poll_shell, daemon=True)
        shell_thread.start()
        try:
            while True: time.sleep(60)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

def get_monitor_status():
    if not os.path.exists(PID_FILE): return "Offline"
    try:
        with open(PID_FILE, "r") as f: pid = int(f.read().strip())
        os.kill(pid, 0)
        return f"Active (PID: {pid})"
    except: return "Offline (Stale)"

def stop_monitor():
    """Stops the background monitor process."""
    if not os.path.exists(PID_FILE):
        print("[!] No monitor process found.")
        return
    try:
        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())
        os.kill(pid, 15) # SIGTERM
        os.remove(PID_FILE)
        print(f"[v] Stopped monitor (PID: {pid})")
    except Exception as e:
        print(f"Error stopping monitor: {e}")

def tail_logs(follow=False, limit=10):
    """Prints the enriched ingestion logs."""
    from rich.console import Console
    from rich.text import Text
    console = Console()
    log_file = os.path.join(os.path.dirname(__file__), "../enriched_logs.json")
    if not os.path.exists(log_file):
        console.print("[bold red][!][/bold red] No enriched logs found yet.")
        return

    def print_log_entry(entry):
        ts = entry.get("timestamp", "")[11:19]
        cat = entry.get("clide_metadata", {}).get("category", "NICHE")
        msg = entry.get("message", "")
        
        color = "white"
        if cat == "FACT": color = "bold green"
        elif cat == "TODO": color = "bold yellow"
        elif cat == "NEW_COMMAND": color = "bold blue"
        elif cat == "TOOL_INTENT": color = "bold magenta"
        
        text = Text()
        text.append(f"[{ts}] ", style="dim")
        text.append(f"{cat:12}", style=color)
        text.append(" | ", style="dim")
        text.append(msg)
        console.print(text)

    with open(log_file, "r") as f:
        try:
            data = json.load(f)
            for entry in data[-limit:]: # Show last N
                print_log_entry(entry)
        except: pass

    if follow:
        print("\n--- Tailing Logs (Ctrl+C to stop) ---")
        import time
        last_size = os.path.getsize(log_file)
        try:
            while True:
                curr_size = os.path.getsize(log_file)
                if curr_size > last_size:
                    with open(log_file, "r") as f:
                        data = json.load(f)
                        print_log_entry(data[-1])
                    last_size = curr_size
                time.sleep(1)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    ClideExtractor().run()