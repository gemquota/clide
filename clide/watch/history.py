import json
import os
import glob
import sqlite3
import re
from datetime import datetime
from intent_classifier import classify_intent # Keeping import for type ref
from vector_registry import get_embeddings
from commands_loader import load_commands
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from llm_utils import call_llm

from config_loader import get_path

MEMORY_DB_PATH = get_path("memory") or os.path.join(os.path.dirname(__file__), "memory.db")
PROGRESS_PATH = os.path.join(os.path.dirname(__file__), "../ingestion_logs/progress.md")
REPORT_GEN_PATH = os.path.join(os.path.dirname(__file__), "report_generator.py")

def update_progress(current, total, active_session):
    try:
        conn = sqlite3.connect(MEMORY_DB_PATH)
        db_count = conn.execute("SELECT COUNT(DISTINCT session_id) FROM knowledge").fetchone()[0]
        conn.close()
        display_processed = max(current, db_count)
    except:
        display_processed = current

    percent = (display_processed / total) * 100 if total > 0 else 100
    with open(PROGRESS_PATH, "w") as f:
        f.write(f"# 📈 Ingestion Progress\n\n")
        f.write(f"- **Total Sessions:** {total}\n")
        f.write(f"- **Processed:** {display_processed}\n")
        f.write(f"- **Status:** {percent:.1f}%\n")
        f.write(f"- **Active Session:** `{active_session[:8] if active_session else 'unknown'}`  \n")
        f.write(f"- **Last Update:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def get_session_files():
    tmp_dir = "/data/data/com.termux/files/home/.gemini/tmp"
    session_files = sorted(glob.glob(os.path.join(tmp_dir, "*/chats/session-*.json")), key=os.path.getmtime)
    active_logs = glob.glob(os.path.join(tmp_dir, "*/logs.json"))
    return session_files, active_logs

def process_batch(tasks, existing_commands):
    """Processes a chunk of messages using hyper-batch LLM calls and batch embeddings."""
    try:
        messages = [t[0] for t in tasks]
        session_ids = [t[1] for t in tasks]
        
        contents = []
        for msg in messages:
            c = msg.get("content", msg.get("message", "")).replace("\n", " ").strip()
            contents.append(c)

        if not contents: return []

        # 1. Hyper-Batch Intent Classification
        # We use a very compressed prompt to reduce output tokens and speed up inference
        commands_summary = ",".join(existing_commands.keys())
        msgs_block = "\n".join([f"{i}:{c[:200]}" for i, c in enumerate(contents)])
        
        prompt = f"""
Classify {len(contents)} msgs for CLIDE. 
Cmds:{commands_summary}. Cats: MATCH,TOOL_INTENT,NEW_COMMAND,FACT,DISCOVERY,LESSON,TODO,NICHE.
Msgs:
{msgs_block}
Return JSON array of objects: {{"cat":"...","cmd":"...","reason":"...","tags":[],"cont":"...","imp":5}}"""

        output = call_llm(prompt)
        json_match = re.search(r'\[.*\]', output, re.DOTALL)
        if not json_match: return []
        analyses = json.loads(json_match.group(0))

        if len(analyses) != len(contents):
            # Partial match handling
            analyses = (analyses + [{"cat":"NICHE"}] * len(contents))[:len(contents)]

        # 2. Batch Embeddings (The real speed)
        distilled_contents = []
        for i, a in enumerate(analyses):
            val = a.get("cont") or a.get("content") or contents[i]
            if not val.strip(): val = contents[i] # Last resort fallback
            distilled_contents.append(val)
            
        embeddings = get_embeddings(distilled_contents)

        results = []
        for i, analysis in enumerate(analyses):
            emb_blob = json.dumps(embeddings[i]).encode('utf-8')
            results.append({
                "session_id": session_ids[i],
                "original_msg": contents[i],
                "category": analysis.get("cat", analysis.get("category", "NICHE")),
                "content": distilled_contents[i],
                "review": analysis.get("reason", analysis.get("reasoning", "")),
                "tags": json.dumps(analysis.get("tags", [])),
                "importance": analysis.get("imp", analysis.get("importance", 5)),
                "embedding": emb_blob,
                "timestamp": messages[i].get("timestamp") or datetime.now().isoformat(),
                "command_name": analysis.get("cmd", analysis.get("command_name"))
            })
        return results
    except Exception as e:
        return []

def ingest_history(max_workers=15, batch_size=20):
    print(f"⚡ OMEGA SPEED INGESTION (Batch: {batch_size}, Threads: {max_workers}) ⚡")
    
    session_files, active_logs = get_session_files()
    existing_commands = load_commands()
    
    pending_tasks = []
    print("  [1/3] Rapid Scanning...")
    conn = sqlite3.connect(MEMORY_DB_PATH)
    
    def is_slop(text):
        if len(text) < 5: return True
        if text.lower() in ["hi", "hello", "test", "ok", "yes", "no"]: return True
        return False

    # Flatten all user messages
    all_msgs = []
    for f_path in session_files:
        try:
            with open(f_path, "r") as f:
                d = json.load(f)
                sid = d.get("sessionId")
                for m in d.get("messages", []):
                    if m.get("type") == "user": all_msgs.append((m, sid))
        except: continue
    for f_path in active_logs:
        try:
            with open(f_path, "r") as f:
                d = json.load(f)
                sid = d[0].get("sessionId") if d else "active"
                for m in d:
                    if m.get("type") == "user": all_msgs.append((m, sid))
        except: continue

    # Filter already processed + slop
    for msg, sid in all_msgs:
        content = msg.get("content", msg.get("message", "")).replace("\n", " ").strip()
        if is_slop(content): continue
        cursor = conn.execute("SELECT 1 FROM knowledge WHERE session_id = ? AND original_msg = ?", (sid, content))
        if not cursor.fetchone():
            pending_tasks.append((msg, sid))
    conn.close()
    
    if not pending_tasks:
        print("🦞 Brain is already full."); return

    # 2. Process in Batches
    import time
    start_time = time.time()
    print(f"  [2/3] Hyper-Processing {len(pending_tasks)} messages...")
    chunks = [pending_tasks[i:i + batch_size] for i in range(0, len(pending_tasks), batch_size)]
    
    total_msg_processed = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_batch, chunk, existing_commands): chunk for chunk in chunks}
        completed = 0
        for future in as_completed(futures):
            res = future.result()
            if res: 
                # Incremental Commit
                conn = sqlite3.connect(MEMORY_DB_PATH, timeout=60)
                try:
                    conn.execute("PRAGMA journal_mode = WAL")
                    conn.execute("PRAGMA synchronous = NORMAL")
                    for r in res:
                        try:
                            conn.execute("INSERT INTO knowledge (category, content, original_msg, importance, embedding, timestamp, session_id, review, tags, command_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                         (r["category"], r["content"], r["original_msg"], r["importance"], r["embedding"], r["timestamp"], r["session_id"], r["review"], r["tags"], r["command_name"]))
                        except: pass
                    conn.commit()
                    total_msg_processed += len(res)
                finally:
                    conn.close()
            
            completed += 1
            elapsed = time.time() - start_time
            rate = total_msg_processed / elapsed if elapsed > 0 else 0
            print(f"    [Heartbeat] Batch {completed}/{len(chunks)} | Saved: {total_msg_processed} | Rate: {rate:.1f} msg/s")
            # Update progress file
            update_progress(total_msg_processed, len(pending_tasks), res[0]["session_id"] if res else "unknown")

    print(f"  [3/3] Omega Finalization...")

    print("  [Final] Pulse Check...")
    subprocess.run(["python3", REPORT_GEN_PATH])
    print("⚡ OMEGA INGESTION COMPLETE. Braine is Optimized. ⚡")

if __name__ == "__main__":
    ingest_history()
            