import http.server
import socketserver
import os
import sys

PORT = 8080
DIRECTORY = "viz"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

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
    # Ensure directory exists
    if not os.path.exists(DIRECTORY):
        print(f"Error: Directory '{DIRECTORY}' not found.")
        sys.exit(1)
        
    start_server()
