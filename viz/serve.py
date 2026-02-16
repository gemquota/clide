import http.server
import socketserver
import os
import sys
import json
import importlib
import subprocess
import threading

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
        # ... existing endpoints ...
        if self.path == '/api/monitor/start':
            global monitor_process
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
            global monitor_process
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
        if self.path == '/api/monitor/status':
            global monitor_process
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            is_running = monitor_process is not None and monitor_process.poll() is None
            self.wfile.write(json.dumps({"running": is_running}).encode())
            return

        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                sys.path.append(os.getcwd())
                # Use centralized db_manager for status too if possible, 
                # but state_manager has more project-wide info.
                state_manager = force_import('swarm.core.state_manager')
                messages = state_manager.get_messages(limit=20, status=None)
                messages.reverse() 
                status_summary = state_manager.get_project_status()

                tracks = []
                try:
                    with open('conductor/tracks.md', 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            if line.startswith('- ['):
                                status_char = line[3]
                                track_name = line.split('**Track: ')[1].split('**')[0]
                                tracks.append({"name": track_name, "status": "done" if status_char == 'x' else "in-progress" if status_char == '~' else "todo"})
                except: pass
                
                response = {
                    "messages": messages,
                    "status_summary": status_summary,
                    "tracks": tracks
                }
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return
            
        if self.path == '/api/knowledge':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            try:
                sys.path.append(os.path.join(os.getcwd(), 'clide'))
                db_manager = force_import('db_manager')
                nodes = db_manager.get_knowledge(limit=50)
                # Convert sqlite rows to list of dicts
                result = [dict(row) for row in nodes]
                self.wfile.write(json.dumps(result).encode())
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

        # Fallback to original
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
