import subprocess
import json

def generate_command_template(command_name, description, user_request):
    prompt = f"""
You are an expert prompt engineer for an AI agent CLI. 
Your goal is to generate a high-quality "System Prompt" for a new command definition.

Command Name: {command_name}
Description: {description}
Original User Request: "{user_request}"

The output must be a TOML-compatible string structure with two keys:
1. `description` (The short description provided above)
2. `prompt` (The complex system prompt)

Requirements for the `prompt`:
- Define a clear **Persona** (e.g., "ACT AS: Python Expert").
- Set **Context** relevant to the task (e.g., "User is on Android/Termux").
- Define **Rules** (e.g., "Be concise", "Use specific tools").
- Define **Response Style** (e.g., "Concise", "Code blocks").
- End with "SYSTEM ONLINE. AWAITING INPUT."

Return ONLY the raw prompt content (the string that goes inside the `prompt = \"\"\" ... \"\"\"` block). Do not return the full TOML, just the inner text for the prompt variable.
"""

    try:
        result = subprocess.run(
            ["gemini", "-p", prompt],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error generating template: {e}"

if __name__ == "__main__":
    # Test
    print(generate_command_template("test_cmd", "Tests the generator", "Make a command that tests things"))
