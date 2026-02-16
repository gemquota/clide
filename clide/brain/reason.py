import subprocess
import json
import os

def classify_intent(message, existing_commands):
    # Prepare the prompt for the classifier
    commands_summary = "\n".join([f"- {name}: {info['description']}" for name, info in existing_commands.items()])
    
    prompt = f"""
Analyze the following user request and determine its intent for the CLIDE Extraction Engine.
User Request: "{message}"

Existing Commands:
{commands_summary}

Classify the request into EXACTLY ONE of these categories:
1. MATCH: Matches an existing command.
2. TOOL_INTENT: A request to build a new technical tool, script, or MCP server.
3. NEW_COMMAND: A clear, reusable task/tool that doesn't fit the 'TOOL_INTENT' (e.g. higher-level behavioral commands).
4. FACT: Personal info, preferences, or environment details (e.g., "I use ZSH", "The project root is X").
5. DISCOVERY: Technical insights, useful shell snippets, or "how-to" notes.
6. LESSON: A mistake to avoid, a correction, or a stylistic preference.
7. TODO: A task or reminder that needs tracking.
8. NICHE: Too specific, one-off, or conversational.

Return ONLY a JSON object with this structure (STRICT_JSON_ENFORCEMENT - No markdown, no preamble):
{{
  "category": "MATCH | TOOL_INTENT | NEW_COMMAND | FACT | DISCOVERY | LESSON | TODO | NICHE",
  "command_name": "string or null",
  "tool_name": "string or null (Required for TOOL_INTENT)",
  "logic_code": "string or null (Required for TOOL_INTENT - The actual python/bash/etc logic)",
  "reasoning": "Why you chose this category",
  "tags": ["list", "of", "relevant", "tags"],
  "content": "A cleaned/formalized version of the information to be saved",
  "importance": 5,
  "complexity": 1,
  "suggested_description": "string or null"
}}"""

    # Call gemini API via utils
    try:
        from clide.brain.model import call_llm
        output = call_llm(prompt)
        
        if not output:
             return {"category": "ERROR", "reasoning": "Model returned empty output (Possible timeout or crash)."}

        # Robust JSON extraction
        try:
            # 1. Try finding JSON block wrapped in ```json ... ```
            import re
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', output, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # 2. Try finding the first outer curly braces
                start = output.find('{')
                end = output.rfind('}') + 1
                if start != -1 and end > start:
                    json_str = output[start:end]
                else:
                    # 3. Fallback: Assume the whole string is JSON (risky but possible)
                    json_str = output
            
            data = json.loads(json_str)
            # Ensure required fields exist to avoid KeyErrors elsewhere
            if "category" not in data:
                data["category"] = "NICHE"
            return data
        except json.JSONDecodeError as e:
             print(f"[Debug] JSON Parse Error: {e}")
             return {"category": "ERROR", "reasoning": f"Model returned invalid JSON: {output[:100]}..."}

            
    except Exception as e:
        return {"category": "ERROR", "reasoning": str(e)}

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
        from clide.brain.model import call_llm
        output = call_llm(prompt)
        start = output.find('{')
        end = output.rfind('}') + 1
        if start != -1 and end != 0:
            return json.loads(output[start:end])
    except:
        pass
    return {"category": "NICHE"}

if __name__ == "__main__":
    # Test
    test_commands = {"engineer": {"description": "Activates the Termux Engineer persona"}}
    test_msg = "Can you help me optimize my termux setup?"
    print(classify_intent(test_msg, test_commands))
