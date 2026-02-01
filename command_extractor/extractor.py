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
from hotswapper import hotswap_mcp_server

STATE_FILE = "/data/data/com.termux/files/home/meta/command_extractor/state.json"
SHELL_STATE_FILE = "/data/data/com.termux/files/home/meta/command_extractor/shell_state.json"

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
    # Look for /command patterns
    cmds = re.findall(r'/(\w+)', text)
    for c in cmds:
        state["usage_stats"][c] = state["usage_stats"].get(c, 0) + 1
        if state["usage_stats"][c] == 5:
            print(f"\n[!] PROMOTION ALERT: '{c}' has been used 5 times.")
            print(f"Suggestion: Promote '{c}' to a full MCP Skill for better performance.")

def get_contextual_suggestions():
    files = os.listdir(".")
    context = " ".join(files[:10]) # Use first 10 files as context
    print(f"\n[Context] Current directory contains: {context[:50]}...")
    results = search_registry(context, limit=2)
    if results and results[0][0] > 0.4:
        print(f"Recommended tools for this environment:")
        for sim, item in results:
            print(f"  - {item['id']} ({item['metadata']['desc']})")

def handle_analysis(analysis, original_input):
    category = analysis.get('category', 'NICHE')
    if category == "NEW_COMMAND":
        cmd_name = analysis.get('command_name')
        cmd_desc = analysis.get('suggested_description')
        raw_logic = analysis.get('raw_logic', original_input)
        
        similar = search_registry(cmd_desc, limit=1)
        if similar and similar[0][0] > 0.85:
            sim, item = similar[0]
            print(f"WARNING: Potential duplicate found ({int(sim*100)}% match): '{item['id']}'")
            cont = input(f"[?] Still create '{cmd_name}'? (y/N): ").strip().lower()
            if cont != 'y': return

        print(f"\n>>> DETECTED POTENTIAL AGENTIC ASSET <<<")
        print(f"Name: {cmd_name} | Desc: {cmd_desc}")
        
        try:
            choice = input(f"[?] Save as (T)OML Command, (M)CP Server, or (N)ext? [t/m/n]: ").strip().lower()
            if choice == 't':
                system_prompt = generate_command_template(cmd_name, cmd_desc, original_input)
                save_new_command(cmd_name, cmd_desc, system_prompt)
                add_to_registry(cmd_name, {"type": "toml", "desc": cmd_desc}, f"{cmd_name} {cmd_desc}")
            elif choice == 'm':
                mcp_content = get_python_mcp_template(cmd_name, cmd_desc, cmd_name, cmd_desc, raw_logic)
                mcp_path = os.path.join("/data/data/com.termux/files/home/meta/commands/mcp_servers", f"{cmd_name}.py")
                save_mcp_server(cmd_name, mcp_content)
                add_to_registry(cmd_name, {"type": "mcp", "path": mcp_path, "desc": cmd_desc}, f"{cmd_name} {cmd_desc}")
                hotswap_mcp_server(cmd_name, mcp_path)
        except EOFError: pass

def monitor():
    print("Initializing CLIDE v0.4.8 (Command Line Interface - Database: Everything)...")
    print("Status: Active. Usage Tracking, Contextual Loading, & Self-Refactoring enabled.")
    
    state = load_state()
    last_id = state.get("last_message_id", -1)
    
    # Run a context check on startup
    get_contextual_suggestions()
    
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
                        if len(text.split()) < 4 or "monitor gemini" in text.lower():
                            last_id = msg["messageId"]
                            continue
                        print(f"\n[Neural Stream] Analyzing Message {msg['messageId']}...")
                        analysis = classify_intent(text, existing_commands)
                        handle_analysis(analysis, text)
                        last_id = msg["messageId"]
                    state["last_message_id"] = last_id
                    save_state(state)
            except Exception as e:
                print(f"Neural Stream Error: {e}")

        time.sleep(10)

if __name__ == "__main__":
    monitor()