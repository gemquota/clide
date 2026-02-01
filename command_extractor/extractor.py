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
    cmds = re.findall(r'/(\w+)', text)
    for c in cmds:
        state["usage_stats"][c] = state["usage_stats"].get(c, 0) + 1
        if state["usage_stats"][c] == 5:
            print(f"\n[!] PROMOTION ALERT: '{c}' has been used 5 times.")
            print(f"Suggestion: Promote '{c}' to a full MCP Skill for better performance.")

def get_contextual_suggestions():
    try:
        files = os.listdir(".")
        context = " ".join(files[:10])
        results = search_registry(context, limit=2)
        if results and results[0][0] > 0.4:
            print(f"\n[Context] Recommended tools for this environment:")
            for sim, item in results:
                print(f"  - {item['id']} ({item['metadata']['desc']})")
    except: pass

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
        
        # Security Audit Phase (v0.6.0 Objective B)
        audit = audit_asset(cmd_name, raw_logic)
        rating = audit.get("rating", "UNKNOWN")
        print(f"\n[Security Audit] Rating: {rating}")
        if rating != "SAFE":
            for risk in audit.get("risks", []):
                print(f"  - WARNING: {risk}")
            print(f"  - Mitigation: {audit.get('mitigation')}")
            cont = input(f"[?] Proceed despite security warnings? (y/N): ").strip().lower()
            if cont != 'y': return

        try:
            choice = input(f"[?] Save as (T)OML Command, (M)CP Server, or (N)ext? [t/m/n]: ").strip().lower()
            if choice == 't':
                system_prompt = generate_command_template(cmd_name, cmd_desc, original_input)
                save_new_command(cmd_name, cmd_desc, system_prompt)
                add_to_registry(cmd_name, {"type": "toml", "desc": cmd_desc}, f"{cmd_name} {cmd_desc}")
                save_provenance(cmd_name, original_input)
                commit_asset(cmd_name, "TOML Command")
            elif choice == 'm':
                mcp_content = get_python_mcp_template(cmd_name, cmd_desc, cmd_name, cmd_desc, raw_logic)
                
                # Auto-Repair / Healer Loop (v0.6.0 Objective A)
                print(f"[*] Running dry-run for '{cmd_name}'...")
                from hotswapper import dry_run_mcp, self_repair_mcp
                success, error_log = dry_run_mcp(mcp_content)
                
                if not success:
                    print(f"[!] Dry-run failed. Initiating Self-Repair...")
                    mcp_content = self_repair_mcp(mcp_content, error_log)
                    # Second pass
                    success, error_log = dry_run_mcp(mcp_content)
                    if success:
                        print(f"[v] Self-Repair successful.")
                    else:
                        print(f"[X] Self-Repair failed. Saving anyway for manual fix.")

                mcp_path = os.path.join("/data/data/com.termux/files/home/meta/commands/mcp_servers", f"{cmd_name}.py")
                save_mcp_server(cmd_name, mcp_content)
                add_to_registry(cmd_name, {"type": "mcp", "path": mcp_path, "desc": cmd_desc}, f"{cmd_name} {cmd_desc}")
                save_provenance(cmd_name, original_input)
                hotswap_mcp_server(cmd_name, mcp_path)
                commit_asset(cmd_name, "MCP Server")
        except EOFError: pass

def monitor():
    print("Initializing CLIDE v0.5.0 (Command Line Interface - Database: Everything)...")
    print("Status: Active. Full Repository Syncing enabled.")
    
    state = load_state()
    last_id = state.get("last_message_id", -1)
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

        new_shell_cmds, total_count = get_new_commands(load_state().get("last_shell_count", 0))
        time.sleep(10)

if __name__ == "__main__":
    monitor()