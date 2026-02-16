import sqlite3
import os
import json
import glob
import csv
from datetime import datetime

from config_loader import get_path

DB_PATH = get_path("memory") or os.path.join(os.path.dirname(__file__), "memory.db")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../ingestion_logs")
CHUNK_SIZE = 200 * 1024 # 200 KB

def clean_txt(text):
    if not text: return ""
    return str(text).replace("\n", " ").replace("|", "\\|")

def write_chunked(subdir, base_filename, title, intro, cards):
    part = 1
    dir_path = os.path.join(OUTPUT_DIR, subdir)
    os.makedirs(dir_path, exist_ok=True)
    
    current_content = f"# {title}\n\n{intro}\n\n---\n"
    
    for card in cards:
        if not card: continue
        if len(current_content.encode('utf-8')) + len(card.encode('utf-8')) > CHUNK_SIZE:
            with open(os.path.join(dir_path, f"{base_filename}_part{part:02d}.md"), "w") as f:
                f.write(current_content)
            part += 1
            current_content = f"# {title} (Part {part})\n\n---\n" + card
        else:
            current_content += card
            
    with open(os.path.join(dir_path, f"{base_filename}_part{part:02d}.md"), "w") as f:
        f.write(current_content)

def generate_main_log():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT category, original_msg, review, tags, importance, session_id, timestamp FROM knowledge ORDER BY timestamp ASC")
    
    # Group by month
    monthly_cards = {}
    
    current_session = None
    for row in cursor.fetchall():
        cat, msg, review, tags_json, imp, sid, ts = row
        
        if not ts: ts = "2026-01-01 00:00:00" # Fallback
        sid = sid or "UNKNOWN"

        # Detect month
        parts = ts.split("-")
        if len(parts) < 2:
            month_str = "2026-02"
        else:
            month_str = parts[0] + "-" + parts[1]
            
        if month_str not in monthly_cards: monthly_cards[month_str] = []
        
        try:
            tags = ", ".join(json.loads(tags_json)) if tags_json else ""
        except:
            tags = ""
        
        card = ""
        if sid != current_session:
            current_session = sid
            # Ensure we have a valid timestamp string for split
            date_part = ts.split('T')[0] if 'T' in ts else ts.split(' ')[0]
            card += f"\n## 📅 Session: {date_part} (ID: `{sid[:8]}`)\n"
            
        card += f"\n**CATEGORY:** `{cat}`  \n"
        card += "| Ingested Snippet | Review Notes & Logic Reasoning |\n| :--- | :--- |\n"
        card += f"| \"{clean_txt(msg)}\" | {clean_txt(review)} |\n\n"
        card += "| Tags | Imp | Session |\n| :--- | :--- | :--- |\n"
        card += f"| {tags} | {imp} | `{sid[:8]}` |\n\n---\n"
        monthly_cards[month_str].append(card)
    
    for month, cards in monthly_cards.items():
        if not month: continue
        parts = month.split("-")
        year = parts[0]
        m = parts[1] if len(parts) > 1 else "02"
        try:
            month_name = datetime.strptime(m, "%m").strftime("%B")
        except:
            month_name = m
        write_chunked(month, "ingestion_log", f"📂 Development Processing Log: {month_name} {year}", f"Chronological record of Neural Stream ingestion for {month_name} {year}.", cards)
    conn.close()

def generate_new_commands():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT command_name, content, review, tags, session_id, timestamp FROM knowledge WHERE category = 'NEW_COMMAND' ORDER BY timestamp ASC")
    
    global_commands = {}
    monthly_commands = {}
    
    for row in cursor.fetchall():
        cmd_name, content, review, tags_json, sid, ts = row
        
        if not ts: ts = "2026-01-01 00:00:00"
        sid = sid or "UNKNOWN"

        parts = ts.split("-")
        month_str = parts[0] + "-" + parts[1] if len(parts) > 1 else "2026-02"
        
        name = cmd_name or "pending_assignment"
        
        # Global grouping for CSV
        if name not in global_commands:
            global_commands[name] = {"desc": content, "instances": []}
        global_commands[name]["instances"].append({"sid": sid, "review": review, "tags": tags_json})
        
        # Monthly grouping for MD
        if month_str not in monthly_commands: monthly_commands[month_str] = {}
        if name not in monthly_commands[month_str]:
            monthly_commands[month_str][name] = {"desc": content, "instances": []}
        monthly_commands[month_str][name]["instances"].append({"sid": sid, "review": review, "tags": tags_json})

    # Write Global CSV
    csv_path = os.path.join(OUTPUT_DIR, "new_commands_summary.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Command", "Occurrences", "Tags", "Primary Description"])
        writer.writeheader()
        for name, data in global_commands.items():
            all_tags = set()
            for inst in data["instances"]:
                try: 
                    if inst["tags"]:
                        all_tags.update(json.loads(inst["tags"]))
                except: pass
            desc_text = data.get("desc") or ""
            writer.writerow({
                "Command": name,
                "Occurrences": len(data["instances"]),
                "Tags": ", ".join(list(all_tags)),
                "Primary Description": str(desc_text).replace("\n", " ")
            })

    # Write Monthly MDs
    for month, commands in monthly_commands.items():
        parts = month.split("-")
        year = parts[0]
        m = parts[1] if len(parts) > 1 else "02"
        try:
            month_name = datetime.strptime(m, "%m").strftime("%B")
        except:
            month_name = m
            
        summary = f"# 🚀 New Commands Inventory: {month_name} {year}\n\n| Command | Occurrences | Tags | Primary Description |\n| :--- | :--- | :--- | :--- |\n"
        cards = []
        for name, data in commands.items():
            all_tags = set()
            for inst in data["instances"]:
                try:
                    if inst["tags"]:
                        all_tags.update(json.loads(inst["tags"]))
                except: pass
            
            desc_val = data.get('desc')
            desc_preview = clean_txt(str(desc_val)[:100]) if desc_val else "No description available."
            summary += f"| `{name}` | {len(data['instances'])} | {', '.join(list(all_tags)[:3])} | {desc_preview} |\n"
            
            card = f"\n**COMMAND:** `` `{name}` ``  \n"
            card += f"**Primary Definition:** *{desc_val}*  \n\n"
            card += "| Session | Logic Reasoning | Tags |\n| :--- | :--- | :--- |\n"
            for inst in data["instances"]:
                t_str = ""
                try:
                    if inst['tags']:
                        t_str = ", ".join(json.loads(inst['tags']))
                except: pass
                s_id = inst.get('sid') or "UNKNOWN"
                card += f"| `{s_id[:8]}` | {clean_txt(inst.get('review'))} | {t_str} |\n"
            card += "\n---\n"
            cards.append(card)
        
        # Write chunked commands
        write_chunked(month, "new_commands_inventory", f"🚀 New Commands Inventory: {month_name} {year}", summary, cards)

    # --- ALL TIME GRAND TOTAL FOR COMMANDS ---
    summary_all = f"# 🌎 Grand Total Commands Inventory (All Time)\n\n| Command | Occurrences | Tags | Primary Description |\n| :--- | :--- | :--- | :--- |\n"
    cards_all = []
    for name, data in global_commands.items():
        all_tags = set()
        for inst in data["instances"]:
            try:
                if inst["tags"]:
                    all_tags.update(json.loads(inst["tags"]))
            except: pass
        desc_val = data.get('desc')
        desc_preview = clean_txt(str(desc_val)[:100]) if desc_val else "No description available."
        summary_all += f"| `{name}` | {len(data['instances'])} | {', '.join(list(all_tags)[:3])} | {desc_preview} |\n"
        
        card = f"\n**COMMAND:** `` `{name}` ``  \n"
        card += f"**Primary Definition:** *{desc_val}*  \n\n"
        card += "| Session | Logic Reasoning | Tags |\n| :--- | :--- | :--- |\n"
        for inst in data["instances"]:
            t_str = ""
            try:
                if inst['tags']:
                    t_str = ", ".join(json.loads(inst['tags']))
            except: pass
            s_id = inst.get('sid') or "UNKNOWN"
            card += f"| `{s_id[:8]}` | {clean_txt(inst.get('review'))} | {t_str} |\n"
        card += "\n---\n"
        cards_all.append(card)
    
    write_chunked("all", "grand_total_commands", "🌎 Grand Total Commands Inventory", "Complete history of all detected agentic assets.", cards_all)
    conn.close()

def generate_system_roles():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT category, content, review, session_id, timestamp FROM knowledge WHERE category = 'META' OR content LIKE '%role%' OR content LIKE '%persona%' ORDER BY timestamp ASC")
    
    roles = {
        "AUDITOR-ZERO": {"name": "Principal Quality Auditor", "protocol": "Protocol 3.1", "focus": "Quality & Validation", "db": "`review_sessions`", "data": None},
        "STRATEGIST-ZERO": {"name": "Strategic Ledger", "protocol": "Protocol 2.1", "focus": "Idea Funneling", "db": "`ideas`", "data": None},
        "SRE-ZERO": {"name": "Incident State Manager", "protocol": "Protocol 1.2", "focus": "Bug & Incident Resolution", "db": "`incidents`", "data": None},
        "TPM-ZERO": {"name": "Technical Program Manager", "protocol": "Protocol 2.2", "focus": "Architecture & Roadmapping", "db": "`roadmaps`", "data": None}
    }
    
    other_roles_monthly = {}
    all_role_cards = []
    reset_seq = None

    for row in cursor.fetchall():
        cat, content, review, sid, ts = row
        
        if not ts: ts = "2026-01-01 00:00:00"
        sid = sid or "UNKNOWN"
        content = content or ""

        parts = ts.split("-")
        month_str = parts[0] + "-" + parts[1] if len(parts) > 1 else "2026-02"
        
        if month_str not in other_roles_monthly: other_roles_monthly[month_str] = []
        
        # Generic card for "all" time
        generic_card = f"## [{cat}] Session: `{sid[:8]}` ({ts})\n{content}\n*Reasoning:* {review}\n\n---\n"
        all_role_cards.append(generic_card)

        found = False
        for key in roles:
            if key in content:
                roles[key]["data"] = content
                roles[key]["sid"] = sid
                roles[key]["month"] = month_str
                found = True
                break
        if not found:
            if "RESET" in content or "FLUSHED" in content:
                reset_seq = content
            else:
                other_roles_monthly[month_str].append({"cat": cat, "content": content, "review": review, "sid": sid})

    overview = "## 📋 Persona Quick-Reference\n\n| Persona | Protocol | Focus | Primary Table |\n| :--- | :--- | :--- | :--- |\n"
    for key, val in roles.items():
        overview += f"| **{key}** | {val['protocol']} | {val['focus']} | {val['db']} |\n"
    
    monthly_output_cards = {}
    for key, val in roles.items():
        if val.get("data"):
            m = val.get("month", "2026-02")
            if m not in monthly_output_cards: monthly_output_cards[m] = []
            card = f"## 🛠 Role: {key}\n**Definition:** Persistent {val['name']}\n*Ingested from Session: `{val.get('sid', 'UNKNOWN')[:8]}`*\n\n"
            body = val["data"].replace("**Core Directive:**", "### 1. Core Directive\n").replace("### 1. The Persistence Layer", "### 2. The Persistence Layer").replace("### 2. Operational Protocol", "### 3. Operational Protocol").replace("### 3. Interaction Process", "### 4. Interaction Process").replace("**Input Trigger:**", "### 4. Input Trigger\n")
            card += body + "\n\n---\n"
            monthly_output_cards[m].append(card)

    for month, others in other_roles_monthly.items():
        if month not in monthly_output_cards: monthly_output_cards[month] = []
        if others:
            monthly_output_cards[month].append("## 👤 Other Directives & Behavioral Profiles\n\n")
            for r in others:
                monthly_output_cards[month].append(f"**{r['cat']}**: {r['content']}\n*Reasoning:* {r['review']}\n\n---\n")

    if reset_seq:
        latest_month = sorted(monthly_output_cards.keys())[-1] if monthly_output_cards else "2026-02"
        if latest_month not in monthly_output_cards: monthly_output_cards[latest_month] = []
        monthly_output_cards[latest_month].append(f"## ⚠️ SYSTEM OVERRIDE: RESET\n**Definition:** Emergency Sequence\n{reset_seq}\n")

    for month, cards in monthly_output_cards.items():
        parts = month.split("-")
        year = parts[0]
        m = parts[1] if len(parts) > 1 else "02"
        try: month_name = datetime.strptime(m, "%m").strftime("%B")
        except: month_name = m
        final_cards = [overview + "\n---\n"] + cards
        write_chunked(month, "system_roles_inventory", f"🎭 System Roles & Personas: {month_name} {year}", f"**Record of behavioral directives and stateful workflow engines for {month_name} {year}.**", final_cards)
    
    # --- ALL TIME GRAND TOTAL FOR ROLES ---
    write_chunked("all", "grand_total_roles", "🎭 Grand Total System Roles & Personas", "Complete history of behavioral directives and stateful workflow engines.", all_role_cards)
    conn.close()

if __name__ == "__main__":
    generate_main_log()
    generate_new_commands()
    generate_system_roles()