import subprocess
import json

def audit_asset(asset_name, content):
    """Performs a security audit on the logic or prompt using Gemini."""
    prompt = f"""
ACT AS: Security Auditor for Agentic Tools.
Analyze the following asset for security risks (e.g., dangerous shell commands, hardcoded secrets, excessive permissions).

Asset Name: {asset_name}
Content:
{content}

Return ONLY a JSON object:
{{
  "rating": "SAFE | CAUTION | DANGEROUS",
  "risks": ["list of specific risks"],
  "mitigation": "suggested change or advice"
}}
"""
    try:
        result = subprocess.run(["gemini", "-p", prompt], capture_output=True, text=True)
        output = result.stdout.strip()
        start = output.find('{')
        end = output.rfind('}') + 1
        return json.loads(output[start:end])
    except:
        return {"rating": "UNKNOWN", "risks": ["Audit failed"], "mitigation": "Manual review required."}
