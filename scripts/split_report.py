import os

def split_file(file_path, chunk_size_kb=500):
    if not os.path.exists(file_path):
        return
    
    chunk_size = chunk_size_kb * 1024
    base_name, ext = os.path.splitext(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by session headers if possible
    sessions = content.split('\n## 📅 Session Date:')
    header = sessions[0]
    sessions = sessions[1:]
    
    current_chunk = header
    chunk_count = 1
    
    for session in sessions:
        session_text = '\n## 📅 Session Date:' + session
        if len(current_chunk.encode('utf-8')) + len(session_text.encode('utf-8')) > chunk_size and current_chunk != header:
            # Write current chunk
            chunk_file = f"{base_name}_part{chunk_count:02d}{ext}"
            with open(chunk_file, 'w', encoding='utf-8') as cf:
                cf.write(current_chunk)
            print(f"Created {chunk_file}")
            chunk_count += 1
            current_chunk = header + "\n\n(Continued in Part " + str(chunk_count) + ")\n\n" + session_text
        else:
            current_chunk += session_text
            
    # Write the last chunk
    chunk_file = f"{base_name}_part{chunk_count:02d}{ext}"
    with open(chunk_file, 'w', encoding='utf-8') as cf:
        cf.write(current_chunk)
    print(f"Created {chunk_file}")

if __name__ == "__main__":
    split_file('meta/ingestion_report.md')
