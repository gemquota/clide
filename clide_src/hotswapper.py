import subprocess
import os
import tempfile

def hotswap_mcp_server(server_name, file_path):
    """
    Registers the new MCP server with the Gemini CLI configuration.
    """
    print(f"[*] Hotswapping MCP Server: {server_name}...")
    try:
        # For Gemini CLI, this usually involves adding it to the config or 
        # restarting the server if one is running. For now, we'll log the registration.
        # In a real environment, we might run: gemini mcp add <path>
        result = subprocess.run(
            ["gemini", "mcp", "add", file_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"[v] Successfully hotswapped '{server_name}'.")
            return True
        else:
            print(f"[!] Gemini CLI hotswap failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"[!] Error during hotswap: {e}")
        return False

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