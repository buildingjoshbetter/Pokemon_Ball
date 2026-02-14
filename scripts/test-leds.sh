#!/bin/bash
# Test all LED states via the daemon API (no OpenClaw needed)

URL="http://127.0.0.1:8420"

echo "=== PokeBall LED API Test ==="
echo ""

echo "Current status:"
curl -s "$URL/status" | python3 -m json.tool
echo ""

states=("boot" "idle" "agent_active" "tool_call" "success" "error" "disconnected" "idle")

for state in "${states[@]}"; do
    echo "Setting state: $state"
    curl -s -X PUT "$URL/state" \
        -H "Content-Type: application/json" \
        -d "{\"state\": \"$state\"}" | python3 -m json.tool
    sleep 3
done

echo ""
echo "Sending heartbeat..."
curl -s -X POST "$URL/heartbeat" | python3 -m json.tool

echo ""
echo "=== Test complete ==="
