#!/bin/bash
# Full Raspberry Pi setup for PokeBall OpenClaw
# Run this on a fresh Raspberry Pi OS (64-bit Lite) installation.

set -e

echo "============================================"
echo "  PokeBall OpenClaw - Raspberry Pi Setup"
echo "============================================"
echo ""

# --- System Updates ---
echo "[1/6] Updating system packages..."
sudo apt-get update -qq
sudo apt-get upgrade -y -qq

# --- Node.js 22 ---
echo "[2/6] Installing Node.js 22..."
if ! command -v node &> /dev/null || [[ "$(node -v)" != v22* ]]; then
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
    sudo apt-get install -y -qq nodejs
fi
echo "  Node.js $(node -v) installed"

# --- Python dependencies ---
echo "[3/6] Installing Python dependencies..."
sudo apt-get install -y -qq python3-pip python3-venv python3-gpiozero

# --- OpenClaw ---
echo "[4/6] Installing OpenClaw..."
if ! command -v openclaw &> /dev/null; then
    curl -sSL https://get.moltbot.org/install-pi.sh | bash
fi
echo "  OpenClaw installed"

# --- LED Controller ---
echo "[5/6] Installing LED controller daemon..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
chmod +x "$REPO_DIR/led-controller/install.sh"
bash "$REPO_DIR/led-controller/install.sh"

# --- OpenClaw Plugin ---
echo "[6/6] Installing OpenClaw plugin..."
cd "$REPO_DIR/openclaw-plugin"
npm install --quiet
npm run build

PLUGIN_DIR="$HOME/.openclaw/plugins/pokeball-led"
mkdir -p "$PLUGIN_DIR"
cp -r dist/ "$PLUGIN_DIR/"
cp package.json "$PLUGIN_DIR/"

echo ""
echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo ""
echo "  1. Configure Telegram bot:"
echo "     - Message @BotFather on Telegram"
echo "     - Create a new bot with /newbot"
echo "     - Copy the bot token"
echo "     - Edit ~/.openclaw/openclaw.json:"
echo ""
echo '       channels: {'
echo '         telegram: {'
echo '           enabled: true,'
echo '           botToken: "YOUR_BOT_TOKEN_HERE"'
echo '         }'
echo '       }'
echo ""
echo "  2. Enable the PokeBall plugin in ~/.openclaw/openclaw.json:"
echo ""
echo '       plugins: {'
echo '         "pokeball-led": { enabled: true }'
echo '       }'
echo ""
echo "  3. Restart OpenClaw gateway:"
echo "     openclaw gateway restart"
echo ""
echo "  4. Pair your Telegram account:"
echo "     Message your bot on Telegram and approve the pairing code"
echo ""
echo "  5. Test the LEDs:"
echo "     bash $REPO_DIR/scripts/test-leds.sh"
echo ""
echo "  6. Send a message to your bot on Telegram and watch the PokeBall glow!"
