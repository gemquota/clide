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

def rollback_asset(asset_id):
    """Rolls back a specific asset to its previous version in Git."""
    # We need to find the file path for the asset first.
    # We check both commands/ and commands/mcp_servers/
    potential_paths = [
        f"commands/{asset_id}.toml",
        f"commands/mcp_servers/{asset_id}.py"
    ]
    
    found_path = None
    for p in potential_paths:
        if os.path.exists(os.path.join(REPO_DIR, p)):
            found_path = p
            break
            
    if not found_path:
        print(f"Error: Could not find file for asset '{asset_id}'")
        return False

    try:
        os.chdir(REPO_DIR)
        # Revert the file to the previous commit
        result = subprocess.run(["git", "checkout", "HEAD^", "--", found_path], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[v] Successfully rolled back '{asset_id}' to previous version.")
            # Commit the rollback
            subprocess.run(["git", "commit", "-m", f"revert(asset): Rollback '{asset_id}'"], capture_output=True)
            return True
        else:
            print(f"Error: Rollback failed. {result.stderr}")
            return False
    except Exception as e:
        print(f"Error during rollback: {e}")
        return False
