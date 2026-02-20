import http.server
import socketserver
import os
import sys
import json
import importlib
import subprocess
import threading
import markdown

PORT = 8080
DIRECTORY = "viz"

# Global monitor process reference
monitor_process = None

def force_import(module_name):
    if module_name in sys.modules:
        return importlib.reload(sys.modules[module_name])
    return importlib.import_module(module_name)

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        global monitor_process
        # ... existing endpoints ...
        if self.path == '/api/monitor/start':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if monitor_process and monitor_process.poll() is None:
                self.wfile.write(json.dumps({"status": "running"}).encode())
                return

            try:
                # Start monitor in background
                monitor_process = subprocess.Popen([sys.executable, "clide/extractor.py"])
                self.wfile.write(json.dumps({"status": "started", "pid": monitor_process.pid}).encode())
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

        if self.path == '/api/monitor/stop':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if monitor_process:
                monitor_process.terminate()
                monitor_process = None
                self.wfile.write(json.dumps({"status": "stopped"}).encode())
            else:
                self.wfile.write(json.dumps({"status": "not_running"}).encode())
            return

        # Original Persona endpoint
        if self.path == '/api/config/persona':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data)
            content = params.get("content")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                with open('clide/active_persona.toml', 'w') as f:
                    f.write(content)
                self.wfile.write(json.dumps({"status": "updated"}).encode())
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

        # Original Delete endpoint
        if self.path == '/api/knowledge/delete':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data)
            node_id = params.get("node_id")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                sys.path.append(os.getcwd())
                state_manager = force_import('swarm.core.state_manager')
                result = state_manager.delete_knowledge(node_id)
                self.wfile.write(json.dumps({"status": "deleted", "message": result}).encode())
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

    def do_GET(self):
        if self.path == '/api/docs/tree':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            docs_root = os.path.join(os.getcwd(), 'docs', 'cli')
            tree = {}
            top_level = []
            
            if os.path.exists(os.path.join(os.getcwd(), 'docs', 'atlas.md')):
                top_level.append({'name': 'ATLAS (Master)', 'path': 'atlas.md', 'type': 'file'})
            
            for root, dirs, files in os.walk(docs_root):
                rel_path = os.path.relpath(root, docs_root)
                if rel_path == '.':
                    for f in sorted(files):
                        if f.endswith('.md'):
                            top_level.append({'name': f, 'path': os.path.join('cli', f), 'type': 'file'})
                else:
                    sector = rel_path.split(os.sep)[0]
                    if sector not in tree: tree[sector] = []
                    for f in sorted(files):
                        if f.endswith('.md'):
                            full_rel = os.path.join('cli', rel_path, f)
                            tree[sector].append({'name': f.replace('.md', ''), 'path': full_rel, 'type': 'file'})

            self.wfile.write(json.dumps({'top': top_level, 'sectors': tree}).encode())
            return

        if self.path.startswith('/api/docs/content'):
            from urllib.parse import urlparse, parse_qs
            query = parse_qs(urlparse(self.path).query)
            file_path = query.get('path', [None])[0]
            
            if not file_path:
                self.send_error(400, "Missing path parameter")
                return
                
            full_path = os.path.join(os.getcwd(), 'docs', file_path)
            docs_root = os.path.join(os.getcwd(), 'docs')
            
            # Security check
            if not os.path.abspath(full_path).startswith(docs_root):
                 self.send_error(403, "Access denied")
                 return

            if not os.path.exists(full_path):
                self.send_error(404, "File not found")
                return

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    html = markdown.markdown(content, extensions=['fenced_code', 'tables'])
                    self.wfile.write(html.encode())
            except Exception as e:
                self.wfile.write(f"<h1>Error rendering markdown</h1><p>{str(e)}</p>".encode())
            return

        if self.path == '/api/monitor/status':
            global monitor_process
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            is_running = monitor_process is not None and monitor_process.poll() is None
            self.wfile.write(json.dumps({"running": is_running}).encode())
            return
            
        return super().do_GET()

def start_server():
    global PORT
    while PORT < 8100:
        try:
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                print(f"Serving at port {PORT}")
                httpd.serve_forever()
        except OSError:
            print(f"Port {PORT} in use, trying {PORT + 1}")
            PORT += 1
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    if not os.path.exists(DIRECTORY):
        print(f"Error: Directory '{DIRECTORY}' not found.")
        sys.exit(1)
    start_server()