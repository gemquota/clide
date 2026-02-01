import subprocess
import json
import os

def classify_intent(message, existing_commands):
    # Prepare the prompt for the classifier
    commands_summary = "\n".join([f"- {name}: {info['description']}" for name, info in existing_commands.items()])
    
    prompt = f"""
Analyze the following user request and determine if it warrants an automated command.
User Request: "{message}"\n\nExisting Commands:
{commands_summary}\n\nClassify the request into one of these categories:
1. MATCH: The request matches an existing command. Provide the command name.
2. NEW_COMMAND: The request is a clear, reusable task that doesn't exist. Provide a suggested name and description.
3. NICHE: The request is too specific, one-off, or conversational to be a command.\n\nReturn ONLY a JSON object with the following structure:
{{
  "category": "MATCH | NEW_COMMAND | NICHE",
  "command_name": "string or null",
  "reasoning": "brief explanation",
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
        # Find the JSON block in case there's preamble
        start = output.find('{')
        end = output.rfind('}') + 1
        if start != -1 and end != 0:
            json_str = output[start:end]
            return json.loads(json_str)
        else:
            return {"category": "ERROR", "reasoning": "Could not parse JSON from Gemini output"}
            
    except Exception as e:
        return {"category": "ERROR", "reasoning": str(e)}

if __name__ == "__main__":
    # Test
    test_commands = {"engineer": {"description": "Activates the Termux Engineer persona"}}
    test_msg = "Can you help me optimize my termux setup?"
    print(classify_intent(test_msg, test_commands))
