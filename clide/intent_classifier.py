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
2. NEW_COMMAND: A clear, reusable task/tool that doesn't exist.
3. FACT: Personal info, preferences, or environment details (e.g., "I use ZSH", "The project root is X").
4. DISCOVERY: Technical insights, useful shell snippets, or "how-to" notes.
5. LESSON: A mistake to avoid, a correction, or a stylistic preference.
6. TODO: A task or reminder that needs tracking.
7. NICHE: Too specific, one-off, or conversational.

Return ONLY a JSON object with this structure:
{{
  "category": "MATCH | NEW_COMMAND | FACT | DISCOVERY | LESSON | TODO | NICHE",
  "command_name": "string or null",
  "reasoning": "Why you chose this category",
  "content": "A cleaned/formalized version of the information to be saved (for FACT/DISCOVERY/LESSON/TODO)",
  "importance": "Integer 1-10 (How critical is this for long-term project success/safety?)",
  "complexity": "Integer 1-10 (How many moving parts or edge cases? 1-3=Simple, 4-10=Complex/Package)",
  "suggested_description": "string or null"
}}"""

    # Call gemini CLI
    try:
        # Use -p for prompt mode
        result = subprocess.run(
            ["gemini", "-p", prompt],
            capture_output=True,
            text=True
        )
        
        output = result.stdout.strip()
        
        if not output:
             return {"category": "ERROR", "reasoning": "Model returned empty output (Possible timeout or crash)."}

        # Robust JSON extraction
        try:
            # 1. Try finding JSON block wrapped in ```json ... ```
            import re
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', output, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # 2. Try finding the first outer curly braces
                start = output.find('{')
                end = output.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = output[start:end]
                else:
                    # 3. Fallback: Assume the whole string is JSON (risky but possible)
                    json_str = output
            
            return json.loads(json_str)
        except json.JSONDecodeError:
             return {"category": "ERROR", "reasoning": f"Model returned invalid JSON: {output[:50]}..."}

            
    except Exception as e:
        return {"category": "ERROR", "reasoning": str(e)}

if __name__ == "__main__":
    # Test
    test_commands = {"engineer": {"description": "Activates the Termux Engineer persona"}}
    test_msg = "Can you help me optimize my termux setup?"
    print(classify_intent(test_msg, test_commands))
