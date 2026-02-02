import subprocess
import os

REPO_DIR = "/data/data/com.termux/files/home/meta"

def commit_asset(asset_name, asset_type):
    """Stages and commits a newly created asset to the git repository."""
    try:
        # Move to repo dir
        os.chdir(REPO_DIR)
        
        # Add everything (Gitignore handles the rest)
        subprocess.run(["git", "add", "."], capture_output=True)
        
        # Commit with a descriptive message
        msg = f"feat(asset): Extract new {asset_type} '{asset_name}'"
        result = subprocess.run(["git", "commit", "-m", msg], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[Git] Asset '{asset_name}' successfully committed.")
        else:
            # Check if it was just "nothing to commit"
            if "nothing to commit" in result.stdout:
                pass
            else:
                print(f"[Git] Commit failed: {result.stderr}")
                
    except Exception as e:
        print(f"[Git] Error during sync: {e}")

def rollback_asset_and_memory(asset_id):
    """
    Finds the last commit related to the asset and rolls back.
    """
    print(f"[*] Searching for last commit for '{asset_id}'...")
    try:
        # Find the commit hash for the last change to this asset
        result = subprocess.run(
            ["git", "log", "-n", "1", "--format=%H", "--", f"swarm/commands/{asset_id}.toml"],
            capture_output=True,
            text=True
        )
        commit_hash = result.stdout.strip()
        
        if not commit_hash:
            print(f"[!] No commit history found for '{asset_id}'.")
            return

        print(f"[*] Rolling back to {commit_hash}^...")
        subprocess.run(["git", "checkout", f"{commit_hash}^", "--", "swarm/commands/"], check=True)
        subprocess.run(["git", "checkout", f"{commit_hash}^", "--", "clide_src/memory.db"], check=False)
        
        print(f"[v] Rollback complete for '{asset_id}' and associated memory state.")
    except Exception as e:
        print(f"[!] Rollback failed: {e}")

def rollback_asset(asset_id):
    """Rolls back a specific asset to its previous version in Git."""
    potential_paths = [
        f"swarm/commands/{asset_id}.toml",
        f"swarm/commands/mcp_servers/{asset_id}.py"
    ]
    
    found_path = None
    for p in potential_paths:
        full_p = os.path.join(REPO_DIR, p)
        if os.path.exists(full_p):
            found_path = p
            break
            
    if not found_path:
        print(f"Error: Could not find file for asset '{asset_id}'")
        return False

    try:
        os.chdir(REPO_DIR)
        # Check if the file is tracked
        tracked = subprocess.run(["git", "ls-files", "--error-unmatch", found_path], capture_output=True)
        if tracked.returncode != 0:
            print(f"Error: Asset '{asset_id}' is not tracked by Git. Cannot rollback.")
            return False

        # Revert the file to the state in HEAD (undoes unstaged changes)
        # If we want the *previous* version, we use HEAD^
        result = subprocess.run(["git", "checkout", "HEAD^", "--", found_path], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[v] Successfully rolled back '{asset_id}' to previous version.")
            subprocess.run(["git", "add", found_path], capture_output=True)
            subprocess.run(["git", "commit", "-m", f"revert(asset): Rollback '{asset_id}'"], capture_output=True)
            return True
        else:
            print(f"Error: Rollback failed. {result.stderr}")
            return False
    except Exception as e:
        print(f"Error during rollback: {e}")
        return False
