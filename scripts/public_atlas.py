import os
import subprocess
import time
import sys

# Ensure the Flask server is ready
FLASK_SCRIPT = os.path.join(os.getcwd(), "scripts/serve_atlas.py")

print("\n" + "="*50)
print("🚀 LAUNCHING PUBLIC CODE ATLAS (WEB-ACCESSIBLE)")
print("="*50)

# 1. Start Flask in background
flask_proc = subprocess.Popen([sys.executable, FLASK_SCRIPT])

# 2. Wait for it to spin up
time.sleep(2)

print("\n[*] Establishing secure tunnel via localhost.run...")
print("[*] LOOK FOR THE 'https://*.lhr.life' URL BELOW:")
print("-" * 50)

# 3. Start SSH Tunnel (requires ssh client)
try:
    # This will output the public URL directly to the terminal
    # Use -o StrictHostKeyChecking=no for first-time connections
    subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:localhost:8080", "nokey@localhost.run"])
except KeyboardInterrupt:
    print("\n[!] Shutting down...")
finally:
    flask_proc.terminate()
    print("[v] Server terminated.")