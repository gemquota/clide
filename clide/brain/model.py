import os
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

def call_llm(prompt):
    """Utility to call Gemini API directly using the SDK."""
    if not client:
        return ""
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"LLM Error: {e}")
        return ""
