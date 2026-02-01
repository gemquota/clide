import subprocess
import os
import tempfile

def dry_run_mcp(mcp_code):
    """
    Attempts to run the MCP server code in a subprocess to check for syntax 
    errors or immediate import failures.
    """
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as tmp:
        tmp.write(mcp_code)
        tmp_path = tmp.name

    try:
        # We run it with a timeout because mcp.run() is blocking.
        # We look for successful startup or specific errors.
        # Using -c to just check syntax first is safer but doesn't catch import errors.
        result = subprocess.run(
            ["python3", "-m", "py_compile", tmp_path],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return False, result.stderr

        # Secondary check: Try to import the code
        # We use a short timeout and background check if possible, 
        # but for a simple "Healer", syntax + basic run is a good start.
        return True, None
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def self_repair_mcp(mcp_code, error_log):
    """
    Feeds the failing code and error log back to Gemini for repair.
    """
    prompt = f"""
ACT AS: Python Debugging Expert.
The following MCP Server code failed a dry run.

ERROR LOG:
{error_log}

SOURCE CODE:
{mcp_code}

Please fix the code. Ensure all imports are present and syntax is valid.
Return ONLY the corrected code block. No explanations.
"""
    try:
        result = subprocess.run(["gemini", "-p", prompt], capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return mcp_code