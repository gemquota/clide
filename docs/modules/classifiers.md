# Module: Classifiers

## 1. Intent Classifier (`intent_classifier.py`)
### Logic
Analyzes chat messages. It uses the Gemini CLI to compare a user's request against existing commands.
### Output
Returns a JSON object containing:
- `category`: (MATCH | NEW_COMMAND | NICHE)
- `command_name`: Suggested slug.
- `reasoning`: The "Why".

## 2. Shell Intent Classifier (`shell_intent_classifier.py`)
### Logic
Specifically tuned for shell commands. It looks for "script-worthy" one-liners or complex pipe sequences.
### Output
Identical JSON structure to the standard classifier, but includes `raw_logic` (the original shell command string) to be used as a template baseline.
