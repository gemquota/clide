#!/bin/bash
# scripts/public_atlas.sh

# 1. Start the Code Atlas Flask server in the background
echo "Starting CLIDE Code Atlas on port 8080..."
python scripts/serve_atlas.py &
SERVER_PID=$!

# 2. Wait for it to spin up
sleep 3

# 3. Create a public tunnel using localhost.run (SSH)
echo "Establishing secure tunnel via localhost.run..."
echo "LOOK FOR THE 'https://*.lhr.life' URL BELOW:"
echo "--------------------------------------------------"

ssh -o StrictHostKeyChecking=no -R 80:localhost:8080 nokey@localhost.run > tunnel.log 2>&1 &
TUNNEL_PID=$!

# 4. Give tunnel time to initialize and display URL
sleep 5
echo "Tunnel log output:"
cat tunnel.log

echo "--------------------------------------------------"
echo "If no URL appeared above, check tunnel.log"

# Keep script running to maintain processes
wait $SERVER_PID $TUNNEL_PID
