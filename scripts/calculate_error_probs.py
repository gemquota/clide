import sqlite3
import re
import os
import json
from collections import Counter
from clide.kernel import storage

def get_error_probabilities():
    error_counts = Counter()
    total_errors = 0
    patterns = [
        r"E(\d{3})",
        r"404", r"500", r"403", r"503", r"502", r"408", r"101", r"301"
    ]

    # 1. From Database
    try:
        conn = storage.get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("SELECT content FROM knowledge WHERE category='SHELL_HISTORY' OR category='TOOL_INTENT' OR category='FACT'").fetchall()
        for row in rows:
            content = str(row[0])
            for p in patterns:
                match = re.search(p, content)
                if match:
                    code = match.group(0)
                    if not code.startswith('E'): code = f"E{code}"
                    error_counts[code] += 1
                    total_errors += 1
                    break
        conn.close()
    except: pass

    # 2. From enriched_logs.json
    log_path = "clide/enriched_logs.json"
    if os.path.exists(log_path):
        try:
            with open(log_path, "r") as f:
                import json
                logs = json.load(f)
                for entry in logs:
                    msg = entry.get("message", "")
                    meta = entry.get("clide_metadata", {})
                    content = msg + " " + str(meta)
                    for p in patterns:
                        match = re.search(p, content)
                        if match:
                            code = match.group(0)
                            if not code.startswith('E'): code = f"E{code}"
                            error_counts[code] += 1
                            total_errors += 1
                            break
        except: pass

    probs = {}
    if total_errors > 0:
        for code, count in error_counts.items():
            probs[code] = (count / total_errors) * 100
            
    return probs

if __name__ == "__main__":
    probs = get_error_probabilities()
    for code, pct in sorted(probs.items(), key=lambda x: x[1], reverse=True):
        print(f"{code}: {pct:.1f}%")
