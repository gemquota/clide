import subprocess
import json

def classify_shell_intent(commands_batch):
    if not commands_batch:
        return None

    # Concatenate batch for context
    batch_text = "\n".join(commands_batch)
    
    prompt = f""".analyze this sequence of shell commands executed by a user in Termux.
Determine if this sequence (or a specific command within it) should be formalized into a reusable CLIDE command.

Commands:
{batch_text}

Focus on:
1. Complex one-liners (pipelining, complex flags).
2. Repeated patterns of work.
3. Creation of specific assets or configurations.

Return ONLY a JSON object:
{{
  "category": "NEW_COMMAND | NICHE",
  "command_name": "suggested_slug",
  "suggested_description": "what it does",
  "reasoning": "why this is useful",
  "raw_logic": "the shell logic to use as a baseline"
}}

If none of the commands are worth saving, return category "NICHE".
"""

    try:
        result = subprocess.run(
            ["gemini", "-p", prompt],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        start = output.find('{')
        end = output.rfind('}') + 1
        if start != -1 and end != 0:
            return json.loads(output[start:end])
    except:
        pass
    return {"category": "NICHE"}