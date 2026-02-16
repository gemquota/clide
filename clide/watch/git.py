import subprocess
import json
import os
from intent_classifier import classify_intent
from extractor import handle_analysis, load_state, save_state

def get_latest_commits(last_commit_hash=None):
    cmd = ["git", "log", "--pretty=format:%H%n%s%n%b%n---EXT---"]
    if last_commit_hash:
        cmd.append(f"{last_commit_hash}..HEAD")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if not result.stdout.strip():
            return []
        
        commits = []
        raw_blocks = result.stdout.split("---EXT---")
        for block in raw_blocks:
            lines = block.strip().split("\n")
            if len(lines) >= 2:
                commits.append({
                    "hash": lines[0],
                    "message": " ".join(lines[1:])
                })
        return commits[::-1] # Oldest to newest
    except:
        return []

def monitor_git():
    print("[v] Git Ingestion Active. Scanning for pertinent changes...")
    state = load_state()
    last_hash = state.get("last_git_hash")
    
    new_commits = get_latest_commits(last_hash)
    if not new_commits:
        return

    # Mock commands for the classifier context
    # In a real run, load_commands() would be used
    existing_commands = {} 

    for commit in new_commits:
        print(f"  [Git] Analyzing commit: {commit['hash'][:7]}")
        text = f"Context: Git Commit. Message: {commit['message']}"
        
        # We use the same classifier as the neural stream
        analysis = classify_intent(text, existing_commands)
        
        # If it's pertinent (not NICHE), handle it
        if analysis.get('category') != 'NICHE':
            handle_analysis(analysis, text)
        
        last_hash = commit['hash']

    state["last_git_hash"] = last_hash
    save_state(state)

if __name__ == "__main__":
    monitor_git()
