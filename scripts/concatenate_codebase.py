import os
import sys
from datetime import datetime

def is_binary(file_path):
    """Check if a file is binary by reading its first 1024 bytes."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:
                return True
            # Check for non-text characters
            text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
            return bool(chunk.translate(None, text_chars))
    except:
        return True

def concatenate_codebase(root_dir, output_file_name="codebase_concat.txt"):
    # Exclusion patterns
    exclude_dirs = {'.git', '__pycache__', '.gemini', 'node_modules', 'venv', '.pytest_cache', 'archive', 'ingestion_logs'}
    exclude_files = {'.gitignore', '.cliderc', 'newss.png', output_file_name, 'VERSION', 'CHANGELOG.md'}
    exclude_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.pyc', '.db', '.log', '.ico', '.pdf'}

    output_path = os.path.join(root_dir, output_file_name)
    files_to_process = []

    print(f"[*] Scanning {root_dir}...")

    # First Pass: Collect files and verify they are text
    for root, dirs, files in os.walk(root_dir):
        # Prune excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file in exclude_files:
                continue
            if any(file.endswith(ext) for ext in exclude_extensions):
                continue
            
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, root_dir)
            
            if not is_binary(full_path):
                files_to_process.append((rel_path, full_path))

    # Sort files for a consistent Table of Contents
    files_to_process.sort()

    print(f"[*] Found {len(files_to_process)} text files. Generating {output_file_name}...")

    with open(output_path, 'w', encoding='utf-8') as out:
        # Header
        out.write("=" * 80 + "\n")
        out.write(f"CLIDE CODEBASE CONCATENATION - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write("=" * 80 + "\n\n")

        # Table of Contents
        out.write("TABLE OF CONTENTS\n")
        out.write("-" * 80 + "\n")
        for i, (rel_path, _) in enumerate(files_to_process, 1):
            out.write(f"{i:3}. {rel_path}\n")
        out.write("-" * 80 + "\n\n")

        # Content Pass
        for i, (rel_path, full_path) in enumerate(files_to_process, 1):
            separator = f"\n\n{'#' * 80}\n"
            file_header = f"[{i}] FILE: {rel_path}\n"
            location = f"LOCATION: {full_path}\n"
            out.write(separator)
            out.write(file_header)
            out.write(location)
            out.write("-" * 80 + "\n\n")

            try:
                with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                    out.write(f.read())
            except Exception as e:
                out.write(f"!! ERROR READING FILE: {e}\n")
            
            out.write(f"\n\n{'#' * 80}\n")

    print(f"[v] Success! Codebase concatenated to: {output_path}")

if __name__ == "__main__":
    # If run in scripts/ directory, go up one level
    target_dir = os.getcwd()
    if os.path.basename(target_dir) == "scripts":
        target_dir = os.path.dirname(target_dir)
    
    concatenate_codebase(target_dir)
