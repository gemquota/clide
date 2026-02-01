import os
import re

HISTORY_FILE = os.path.expanduser("~/.zsh_history")

def parse_zsh_history_with_time(line):
    # Zsh format: ": 1706761441:0;command"
    match = re.match(r'^: (\d+):\d+;(.*)', line)
    if match:
        return int(match.group(1)), match.group(2).strip()
    return None, line.strip()

def get_new_commands(last_processed_count):
    if not os.path.exists(HISTORY_FILE):
        return [], 0
    
    try:
        with open(HISTORY_FILE, "rb") as f:
            lines = f.read().decode('utf-8', errors='ignore').splitlines()
    except Exception as e:
        print(f"Error reading history: {e}")
        return [], last_processed_count

    total_lines = len(lines)
    if total_lines <= last_processed_count:
        return [], total_lines
    
    new_lines = lines[last_processed_count:]
    raw_cmds = []
    for l in new_lines:
        t, cmd = parse_zsh_history_with_time(l)
        if cmd and len(cmd) > 3:
            raw_cmds.append((t, cmd))
    
    # Batching logic: Group commands within 60 seconds
    batches = []
    if not raw_cmds:
        return [], total_lines
        
    current_batch = [raw_cmds[0][1]]
    last_time = raw_cmds[0][0]
    
    for i in range(1, len(raw_cmds)):
        t, cmd = raw_cmds[i]
        if t and last_time and (t - last_time < 60):
            current_batch.append(cmd)
        else:
            batches.append(" && ".join(current_batch))
            current_batch = [cmd]
        last_time = t
    
    batches.append(" && ".join(current_batch))
    
    # Filter noise
    noise = ["ls", "cd", "pwd", "clear", "exit", "zsh", "rl"]
    filtered = [b for b in batches if b not in noise]
    
    return filtered, total_lines