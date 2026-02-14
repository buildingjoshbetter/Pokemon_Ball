#!/bin/bash
# PokeBall LED Controller - Install Script
# Run this on the Raspberry Pi to set up the LED daemon.

set -e

INSTALL_DIR="/opt/pokeball-openclaw/led-controller"
SERVICE_NAME="pokeball-leds"

echo "=== PokeBall LED Controller Installer ==="
echo ""

# Check if running on Pi
if ! command -v raspi-config &> /dev/null; then
    echo "WARNING: This doesn't look like a Raspberry Pi."
    echo "The LED controller requires GPIO access. Continuing anyway..."
    echo ""
fi

# Create install directory
echo "[1/5] Creating install directory..."
sudo mkdir -p "$INSTALL_DIR"
sudo chown "$USER:$USER" "$INSTALL_DIR"

# Copy files
echo "[2/5] Copying files..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cp "$SCRIPT_DIR"/led_*.py "$INSTALL_DIR/"
cp "$SCRIPT_DIR"/requirements.txt "$INSTALL_DIR/"

# Create virtual environment
echo "[3/5] Setting up Python virtual environment..."
python3 -m venv "$INSTALL_DIR/venv"
"$INSTALL_DIR/venv/bin/pip" install --quiet --upgrade pip
"$INSTALL_DIR/venv/bin/pip" install --quiet -r "$INSTALL_DIR/requirements.txt"

# Install systemd service
echo "[4/5] Installing systemd service..."
sudo cp "$SCRIPT_DIR/pokeball-leds.service" /etc/systemd/system/
sudo sed -i "s|User=pi|User=$USER|g" /etc/systemd/system/pokeball-leds.service
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"

# Start service
echo "[5/5] Starting LED daemon..."
sudo systemctl start "$SERVICE_NAME"

echo ""
echo "=== Installation complete ==="
echo ""
echo "LED daemon is running on http://127.0.0.1:8420"
echo ""
echo "Quick test:"
echo "  curl -s http://127.0.0.1:8420/status"
echo "  curl -s -X PUT http://127.0.0.1:8420/state -H 'Content-Type: application/json' -d '{\"state\":\"idle\"}'"
echo ""
echo "Service commands:"
echo "  sudo systemctl status $SERVICE_NAME"
echo "  sudo systemctl restart $SERVICE_NAME"
echo "  journalctl -u $SERVICE_NAME -f"
