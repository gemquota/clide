import os
import re

def redact_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Regex for GitHub Personal Access Tokens (classic and fine-grained)
        ghp_pattern = r'ghp_[A-Za-z0-9]{36}'
        ghpat_pattern = r'github_pat_[A-Za-z0-9_]{82,}'
        # Regex for Google API Keys
        google_pattern = r'AIza[A-Za-z0-9_\\\-]{35}'
        # Regex for Generic 'sk_' keys (Short.io, Moltbook, etc)
        sk_pattern = r'sk_[A-Za-z0-9_\-]{20,}'
        # Regex for Apify API Tokens
        apify_pattern = r'apify_api_[A-Za-z0-9]{30,}'
        
        new_content = re.sub(ghp_pattern, 'ghp_REDACTED', content)
        new_content = re.sub(ghpat_pattern, 'github_pat_REDACTED', new_content)
        new_content = re.sub(google_pattern, 'AIza_REDACTED', new_content)
        new_content = re.sub(sk_pattern, 'sk_REDACTED', new_content)
        new_content = re.sub(apify_pattern, 'apify_api_REDACTED', new_content)
        
        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[v] Redacted secrets in: {file_path}")
            return True
    except Exception as e:
        print(f"[!] Error processing {file_path}: {e}")
    return False

def main():
    root_dir = "."
    redacted_count = 0
    for root, dirs, files in os.walk(root_dir):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            file_path = os.path.join(root, file)
            if redact_file(file_path):
                redacted_count += 1
    
    print(f"\n[v] Finished. Redacted secrets in {redacted_count} files.")

if __name__ == "__main__":
    main()

