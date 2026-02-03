import json
import os
import time
import glob
import re
from commands_loader import load_commands
from intent_classifier import classify_intent
from template_generator import generate_command_template
from command_saver import save_new_command
from shell_ingestor import get_new_commands
from shell_intent_classifier import classify_shell_intent
from mcp_generator import get_python_mcp_template, save_mcp_server
from vector_registry import add_to_registry, search_registry
from security_auditor import audit_asset
from hotswapper import hotswap_mcp_server
from git_sync import commit_asset
from provenance import save_provenance

from config_loader import get_path, load_config

config = load_config()
STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")
SHELL_STATE_FILE = os.path.join(os.path.dirname(__file__), "shell_state.json")
RECENT_MESSAGES_FILE = os.path.join(os.path.dirname(__file__), "recent_messages.json")
RECENT_MESSAGES_LIMIT = config["extraction"]["repetition_limit"]
MEMORY_DB_PATH = get_path("memory")

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
    
    # Use a slightly more sophisticated overlap check
    current_keywords = set(re.findall(r'\w{4,}', current_text.lower())) # Words of 4+ chars
    if not current_keywords: return False
    
    match_count = 0
    for msg in recent_messages:
        prev_keywords = set(re.findall(r'\w{4,}', msg.lower()))
        overlap = current_keywords.intersection(prev_keywords)
        # If 50% of keywords match, we consider it similar
        if len(overlap) >= (len(current_keywords) * 0.5):
            match_count += 1
            
    if match_count >= 2: # 3rd instance in the last 100 messages
        return True
    return False

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except: pass
    return {"last_message_id": -1, "usage_stats": {}}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def get_latest_log_file():
    tmp_dir = "/data/data/com.termux/files/home/.gemini/tmp"
    sessions = glob.glob(os.path.join(tmp_dir, "*/"))
    if not sessions: return None
    latest_session = max(sessions, key=os.path.getmtime)
    log_file = os.path.join(latest_session, "logs.json")
    return log_file if os.path.exists(log_file) else None

def track_usage(text, state):
    cmds = re.findall(r'/(\w+)', text)
    for c in cmds:
        state["usage_stats"][c] = state["usage_stats"].get(c, 0) + 1
        if state["usage_stats"][c] == 5:
            print(f"\n[!] PROMOTION ALERT: '{c}' has been used 5 times.")
            print(f"Suggestion: Promote '{c}' to a full MCP Skill for better performance.")

def get_agentic_suggestions():
    try:
        files = os.listdir(".")
        context_query = " ".join(files[:10])
        results = search_registry(context_query, limit=2)
        if results and results[0][0] > 0.4:
            print(f"\n[Context] Recommended agentic tools for this environment:")
            for sim, item in results:
                print(f"  - {item['id']} ({item['metadata']['desc']})")
    except: pass

def init_memory_db():
    import sqlite3
    conn = sqlite3.connect(MEMORY_DB_PATH)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            content TEXT,
            original_msg TEXT,
            importance INTEGER DEFAULT 5,
            embedding BLOB,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER,
            target_id INTEGER,
            rel_type TEXT, -- 'DEPENDS_ON', 'SIMILAR_TO', 'CONTRADICTS'
            FOREIGN KEY(source_id) REFERENCES knowledge(id),
            FOREIGN KEY(target_id) REFERENCES knowledge(id)
        );
    """)
    conn.commit()
    conn.close()

def save_knowledge(category, content, original_msg, importance=5):
    import sqlite3
    import json
    from vector_registry import get_embedding
    
    # Generate embedding for semantic search
    emb = get_embedding(content)
    emb_blob = json.dumps(emb).encode('utf-8')

    conn = sqlite3.connect(MEMORY_DB_PATH)
    conn.execute(
        "INSERT INTO knowledge (category, content, original_msg, importance, embedding) VALUES (?, ?, ?, ?, ?)",
        (category, content, original_msg, importance, emb_blob)
    )
    conn.commit()
    conn.close()
    print(f"  [Memory] Saved {category} (Imp: {importance}): {content[:50]}...")

    # Both Database and File sync for TODOs
    if category == "TODO":
        try:
            with open("/data/data/com.termux/files/home/meta/todo.md", "a") as f:
                f.write(f"- [ ] {content} (Extracted from: {original_msg[:30]}...)\n")
        except: pass

def handle_analysis(analysis, original_input):
    category = analysis.get('category', 'NICHE')
    reasoning = analysis.get('reasoning', 'No reasoning provided.')
    
    # Ongoing Review Feedback
    print(f"  [Result] Category: {category}")
    print(f"  [Reason] {reasoning}")

    if category in ["FACT", "DISCOVERY", "LESSON", "TODO"]:
        content = analysis.get('content', original_input)
        importance = analysis.get('importance', 5)
        save_knowledge(category, content, original_input, importance)
        
        if category == "LESSON":
            print(f"\n[!] LESSON LEARNED: {content}")
            print(f"  [Note] Agentic 'context' refers to prompts, commands, and tools.")
            # Non-blocking notification instead of input()
            print(f"  [Action] Refactor scan skipped (non-interactive mode).")
    
    elif category == "NEW_COMMAND":
        cmd_name = analysis.get('command_name')
        cmd_desc = analysis.get('suggested_description')
        
        # In monitor mode, we should avoid blocking. 
        # For now, we will log the detection and require manual clide command to finalize.
        print(f"\n>>> DETECTED POTENTIAL AGENTIC ASSET <<<")
        print(f"Name: {cmd_name} | Desc: {cmd_desc}")
        print(f"Run 'clide ingest --name {cmd_name}' to review and save.")
        return # Skip interactive part in monitor loop

def monitor():
    print("Initializing CLIDE v0.6.0 (Extraction Core)...")
    print("[Debug] Initializing Memory DB...")
    init_memory_db()
    print("[Debug] Loading State...")
    state = load_state()
    last_id = state.get("last_message_id", -1)
    print("[Debug] Loading Recent Messages...")
    recent_messages = load_recent_messages()
    print("[Debug] Getting Agentic Suggestions...")
    get_agentic_suggestions()
    print("[Debug] Entering Main Loop...")
    
    while True:
        log_file = get_latest_log_file()
        if log_file:
            try:
                with open(log_file, "r") as f:
                    logs = json.load(f)
                new_messages = [m for m in logs if m["type"] == "user" and m["messageId"] > last_id]
                if new_messages:
                    existing_commands = load_commands()
                    for msg in new_messages:
                        text = msg['message']
                        track_usage(text, state)
                        if "monitor gemini" in text.lower():
                            last_id = msg["messageId"]
                            continue
                        
                        print(f"\n[Neural Stream] Seen: '{text}' (ID: {msg['messageId']})")
                        
                        if detect_repetition(text, recent_messages):
                            print(f"  [!] REPETITIVE PATTERN DETECTED")
                            print(f"  [>] Forcing command extraction analysis...")
                            analysis = classify_intent(f"Automate this repetitive task: {text}", existing_commands)
                        else:
                            print(f"  [>] Analyzing...")
                            analysis = classify_intent(text, existing_commands)
                        
                        handle_analysis(analysis, text)
                        
                        recent_messages.append(text)
                        save_recent_messages(recent_messages)
                        
                        # Save state after EVERY message for resilience
                        last_id = msg["messageId"]
                        state["last_message_id"] = last_id
                        save_state(state)
                    
            except Exception as e:
                print(f"Neural Stream Error: {e}")

        new_shell_cmds, total_count = get_new_commands(load_state().get("last_shell_count", 0))
        time.sleep(10)

if __name__ == "__main__":
    monitor()