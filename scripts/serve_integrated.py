import os
import json
import socket
import time
import sqlite3
import psutil
from flask import Flask, jsonify, send_from_directory, request, abort

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "viz"))

# --- KERNEL INTEGRATION ---
from clide.kernel.settings import load_config, get_path, CONFIG_PATH
from clide.brain.memory import get_registry_stats
try:
    from clide.watch.stream import get_monitor_status
except ImportError:
    def get_monitor_status(): return "OFFLINE"

MEMORY_DB_PATH = get_path("memory")

def get_db_connection():
    conn = sqlite3.connect(MEMORY_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- API ENDPOINTS ---

# Global historical tracking
HISTORY_LIMIT = 60
CPU_HISTORY = []
MEM_HISTORY = []

@app.route("/api/config", methods=["GET", "POST"])
def manage_config():
    if request.method == "POST":
        new_config = request.json
        try:
            with open(CONFIG_PATH, "w") as f:
                json.dump(new_config, f, indent=4)
            return jsonify({"status": "success", "config": new_config})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    return jsonify(load_config())

@app.route("/api/stats")
def get_stats():
    global CPU_HISTORY, MEM_HISTORY
    
    stats = get_registry_stats()
    try:
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        
        CPU_HISTORY.append({"time": int(time.time()), "value": cpu})
        MEM_HISTORY.append({"time": int(time.time()), "value": mem})
        
        if len(CPU_HISTORY) > HISTORY_LIMIT: CPU_HISTORY.pop(0)
        if len(MEM_HISTORY) > HISTORY_LIMIT: MEM_HISTORY.pop(0)
    except:
        cpu, mem = 0, 0
    
    return jsonify({
        "system": {
            "cpu": cpu,
            "mem": mem,
            "uptime": int(time.time() - os.path.getmtime(MEMORY_DB_PATH)),
            "monitor": get_monitor_status(),
            "history": {
                "cpu": CPU_HISTORY,
                "mem": MEM_HISTORY
            }
        },
        "neural": stats
    })

@app.route("/api/stream")
def get_stream():
    limit = request.args.get("limit", 20, type=int)
    conn = get_db_connection()
    try:
        rows = conn.execute("SELECT * FROM knowledge ORDER BY timestamp DESC LIMIT ?", (limit,)).fetchall()
    except sqlite3.OperationalError:
        rows = []
    conn.close()
    
    return jsonify([dict(row) for row in rows])

@app.route("/api/docs")
def list_docs():
    docs_root = os.path.join(BASE_DIR, "docs/cli")
    doc_tree = []
    if os.path.exists(docs_root):
        for root, dirs, files in os.walk(docs_root):
            rel_dir = os.path.relpath(root, docs_root)
            for f in files:
                if f.endswith(".md"):
                    path = f if rel_dir == "." else os.path.join(rel_dir, f)
                    doc_tree.append({"name": f.replace(".md", ""), "path": path, "domain": rel_dir if rel_dir != "." else "ROOT"})
    return jsonify(doc_tree)

@app.route("/api/docs/<path:filename>")
def get_doc(filename):
    docs_root = os.path.join(BASE_DIR, "docs/cli")
    safe_path = os.path.join(docs_root, filename)
    if not os.path.exists(safe_path):
        abort(404)
    with open(safe_path, "r", encoding="utf-8") as f:
        return f.read()

@app.route("/api/nodes")
def get_nodes():
    conn = get_db_connection()
    try:
        rows = conn.execute("SELECT id, category, content, importance FROM knowledge LIMIT 1000").fetchall()
    except sqlite3.OperationalError:
        rows = []

    try:
        rel_rows = conn.execute("SELECT source_id, target_id, rel_type FROM relationships").fetchall()
    except sqlite3.OperationalError:
        rel_rows = []
    
    conn.close()
    
    nodes = []
    links = []
    
    for row in rows:
        nodes.append({
            "id": row["id"],
            "name": f"[{row['category']}] ID {row['id']}",
            "group": row["category"],
            "val": row["importance"] or 5,
            "desc": row["content"][:500] if row["content"] else ""
        })
    
    for rel in rel_rows:
        links.append({
            "source": rel["source_id"],
            "target": rel["target_id"],
            "type": rel["rel_type"]
        })
    
    return jsonify({"nodes": nodes, "links": links})

# --- STATIC ROUTES ---

@app.route("/")
def serve_portal():
    return send_from_directory(os.path.join(BASE_DIR, "viz"), "integrated.html")

@app.route("/viz/<path:path>")
def serve_viz(path):
    return send_from_directory(os.path.join(BASE_DIR, "viz"), path)

@app.route("/docs/<path:path>")
def serve_docs_assets(path):
    return send_from_directory(os.path.join(BASE_DIR, "docs"), path)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == "__main__":
    ip = get_local_ip()
    port = 8888
    print("\n" + "="*50)
    print(f"🚀 CLIDE UNIFIED PORTAL STARTING...")
    print(f"🔗 Access: http://{ip}:{port}")
    print("="*50 + "\n")
    app.run(host="0.0.0.0", port=port, debug=False)
