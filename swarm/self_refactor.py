import os
import subprocess

DOCS_DIR = "/data/data/com.termux/files/home/meta/docs/modules"
CODE_DIR = "/data/data/com.termux/files/home/meta/clide_src"

def refactor_docs():
    print("--- CLIDE Self-Refactor: Auditing Docs vs Code ---")
    files = [f for f in os.listdir(CODE_DIR) if f.endswith(".py")]
    
    for code_file in files:
        doc_file = code_file.replace(".py", ".md")
        # Handle naming discrepancies (e.g., extractor.py -> core_monitor.md)
        if code_file == "extractor.py": doc_file = "core_monitor.md"
        
        doc_path = os.path.join(DOCS_DIR, doc_file)
        code_path = os.path.join(CODE_DIR, code_file)
        
        if not os.path.exists(doc_path):
            print(f"[!] Missing documentation for {code_file}. Generating...")
            generate_new_doc(code_path, doc_path)
            continue
            
        with open(code_path, "r") as f: code_content = f.read()
        with open(doc_path, "r") as f: doc_content = f.read()
        
        prompt = f"""
Audit this documentation against the actual source code.
Identify if the documentation is outdated or missing key functions/logic.

Source Code:
{code_content}

Current Documentation:
{doc_content}

If the documentation is accurate, return 'OK'. 
If not, return a fully updated version of the documentation in Markdown format.
"""
        result = subprocess.run(["gemini", "-p", prompt], capture_output=True, text=True)
        response = result.stdout.strip()
        
        if "OK" not in response[:10]:
            print(f"[!] Updating documentation for {code_file}...")
            with open(doc_path, "w") as f:
                f.write(response)
        else:
            print(f"[v] {code_file} documentation is up to date.")

def generate_new_doc(code_path, doc_path):
    with open(code_path, "r") as f: content = f.read()
    prompt = f"Generate a technical documentation file for this Python code in Markdown:\n\n{content}"
    result = subprocess.run(["gemini", "-p", prompt], capture_output=True, text=True)
    with open(doc_path, "w") as f:
        f.write(result.stdout.strip())

if __name__ == "__main__":
    refactor_docs()
