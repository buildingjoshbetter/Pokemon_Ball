#!/bin/bash
# Simulates a full OpenClaw agent lifecycle for demo purposes.
# Run this to show the PokeBall's LED behavior without needing
# a real Telegram message.

URL="http://127.0.0.1:8420"

echo "=== PokeBall Demo Sequence ==="
echo ""
echo "This simulates what happens when you send a Telegram message."
echo "Watch the PokeBall's LEDs as each step fires."
echo ""

# Start: idle
echo "[0s] Agent is idle, waiting for message..."
curl -s -X PUT "$URL/state" -H "Content-Type: application/json" -d '{"state":"idle"}' > /dev/null
sleep 3

# User sends a message
echo "[3s] Message received! Agent starts thinking..."
curl -s -X PUT "$URL/state" -H "Content-Type: application/json" -d '{"state":"agent_active"}' > /dev/null
sleep 2

# Agent calls a tool
echo "[5s] Agent is calling a tool (web search)..."
curl -s -X PUT "$URL/state" -H "Content-Type: application/json" -d '{"state":"tool_call"}' > /dev/null
sleep 3

# Tool returns
echo "[8s] Tool returned, agent is processing results..."
curl -s -X PUT "$URL/state" -H "Content-Type: application/json" -d '{"state":"agent_active"}' > /dev/null
sleep 2

# Agent finishes successfully
echo "[10s] Agent sent response! Success!"
curl -s -X PUT "$URL/state" -H "Content-Type: application/json" -d '{"state":"success"}' > /dev/null
sleep 1

# Back to idle
echo "[11s] Back to idle, waiting for next message..."
curl -s -X PUT "$URL/state" -H "Content-Type: application/json" -d '{"state":"idle"}' > /dev/null
sleep 3

# Simulate an error
echo "[14s] New message... agent starts thinking..."
curl -s -X PUT "$URL/state" -H "Content-Type: application/json" -d '{"state":"agent_active"}' > /dev/null
sleep 2

echo "[16s] Something went wrong! Error state..."
curl -s -X PUT "$URL/state" -H "Content-Type: application/json" -d '{"state":"error"}' > /dev/null
sleep 3

# Recover
echo "[19s] Recovering... back to idle."
curl -s -X PUT "$URL/state" -H "Content-Type: application/json" -d '{"state":"idle"}' > /dev/null

echo ""
echo "=== Demo complete ==="
