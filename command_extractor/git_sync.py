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
