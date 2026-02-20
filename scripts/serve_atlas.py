import os
import socket
import sys
from flask import Flask, render_template_string, send_from_directory, abort

app = Flask(__name__)

# Exclusion patterns
EXCLUDE_DIRS = {'.git', '__pycache__', '.gemini', 'node_modules', 'venv', '.pytest_cache'}
EXCLUDE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.pyc', '.db', '.log', '.ico', '.pdf', '.bin'}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CLIDE // CODE ATLAS</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .sidebar { background-color: #161b22; border-right: 1px solid #30363d; height: 100vh; overflow-y: auto; }
        .content { height: 100vh; overflow-y: auto; background-color: #0d1117; }
        .file-link:hover { background-color: #21262d; color: #58a6ff; }
        .folder-name { color: #8b949e; font-weight: bold; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05rem; }
        pre { border-radius: 8px !important; margin: 0 !important; font-size: 0.9rem !important; }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #161b22; }
        ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #484f58; }
    </style>
</head>
<body class="flex">
    <!-- Sidebar -->
    <div class="sidebar w-80 p-4 flex-shrink-0">
        <div class="mb-6">
            <h1 class="text-xl font-bold text-cyan-400 mb-1">CODE ATLAS</h1>
            <p class="text-xs text-gray-500">CLIDE V1.0.0 // KOS</p>
        </div>
        
        <nav class="space-y-1">
            {% for item in tree %}
                {% if item.type == 'dir' %}
                    <div class="mt-4 mb-1 px-2 folder-name">{{ item.name }}</div>
                {% else %}
                    <a href="/view/{{ item.path }}" class="block px-2 py-1 text-sm file-link rounded transition-colors truncate">
                        {{ item.name }}
                    </a>
                {% endif %}
            {% endfor %}
        </nav>
    </div>

    <!-- Main Content -->
    <div class="content flex-grow p-8">
        {% if filename %}
            <div class="mb-4 flex items-center justify-between">
                <div>
                    <h2 class="text-lg font-mono text-blue-400">{{ filename }}</h2>
                    <p class="text-xs text-gray-500">{{ full_path }}</p>
                </div>
                <a href="/" class="text-xs bg-gray-800 hover:bg-gray-700 px-3 py-1 rounded text-gray-300 transition-colors">BACK TO TOP</a>
            </div>
            <pre class="line-numbers"><code class="language-{{ lang }}">{{ code }}</code></pre>
        {% else %}
            <div class="flex flex-col items-center justify-center h-full opacity-50">
                <div class="text-6xl mb-4">🔭</div>
                <h2 class="text-2xl font-light">Select a file to explore</h2>
                <p class="text-sm mt-2">CLIDE Neural Network Viewer // Read-Only Mode</p>
            </div>
        {% endif %}
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-javascript.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-markdown.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
</body>
</html>
'''

def get_file_tree(root):
    tree = []
    for current_root, dirs, files in os.walk(root):
        # Filter directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        
        rel_dir = os.path.relpath(current_root, root)
        if rel_dir != ".":
            tree.append({"type": "dir", "name": rel_dir, "path": rel_dir})
        
        for f in sorted(files):
            if any(f.endswith(ext) for ext in EXCLUDE_EXTENSIONS) or f.startswith('.'):
                continue
            
            full_path = os.path.join(current_root, f)
            rel_path = os.path.relpath(full_path, root)
            tree.append({"type": "file", "name": f, "path": rel_path})
            
    return tree

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

@app.route("/")
def index():
    tree = get_file_tree(BASE_DIR)
    return render_template_string(HTML_TEMPLATE, tree=tree)

@app.route("/view/<path:filepath>")
def view_file(filepath):
    full_path = os.path.join(BASE_DIR, filepath)
    if not os.path.exists(full_path) or os.path.isdir(full_path):
        abort(404)
    
    try:
        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            code = f.read()
    except Exception as e:
        code = f"Error reading file: {e}"

    ext = os.path.splitext(filepath)[1].lower()
    lang_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.json': 'json',
        '.md': 'markdown',
        '.sh': 'bash',
        '.html': 'html',
        '.css': 'css'
    }
    lang = lang_map.get(ext, 'clike')
    
    tree = get_file_tree(BASE_DIR)
    return render_template_string(
        HTML_TEMPLATE, 
        tree=tree, 
        code=code, 
        filename=os.path.basename(filepath),
        full_path=filepath,
        lang=lang
    )

if __name__ == "__main__":
    ip = get_local_ip()
    port = 8080
    print("\n" + "="*50)
    print(f"🚀 CLIDE CODE ATLAS IS LIVE!")
    print(f"🔗 Local Access:   http://localhost:{port}")
    print(f"🔗 Network Access: http://{ip}:{port}")
    print("="*50 + "\n")
    
    app.run(host="0.0.0.0", port=port, debug=False)