# LED Controller

Python daemon that drives the PokeBall's LEDs based on state commands from the OpenClaw plugin.

## How It Works

The LED controller is a FastAPI server running on `127.0.0.1:8420`. It receives HTTP requests from the OpenClaw plugin and translates them into GPIO signals that control three LEDs (red, green, blue).

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `PUT` | `/state` | Set LED state (`{"state": "idle"}`) |
| `POST` | `/heartbeat` | Heartbeat from OpenClaw plugin |
| `GET` | `/status` | Get current LED state |

### State Machine

The controller uses a stack-aware state machine:

```
BOOT ──────► IDLE ◄──── SUCCESS
               │            ▲
               ▼            │
         AGENT_ACTIVE ──────┘
               │
               ▼
           TOOL_CALL ───► AGENT_ACTIVE (pop stack)

  Any state ──► ERROR
  Any state ──► DISCONNECTED (heartbeat timeout)
```

## Installation

### On the Raspberry Pi

```bash
chmod +x install.sh
./install.sh
```

This installs the daemon to `/opt/pokeball-openclaw/led-controller/`, creates a Python virtual environment, and sets up a systemd service that starts on boot.

### Manual Test

```bash
# Test LED wiring
python3 test_leds.py

# Test the daemon
uvicorn led_daemon:app --host 127.0.0.1 --port 8420

# In another terminal:
curl -X PUT http://127.0.0.1:8420/state \
  -H "Content-Type: application/json" \
  -d '{"state": "agent_active"}'
```

## Files

| File | Description |
|------|-------------|
| `led_daemon.py` | FastAPI server + heartbeat watchdog |
| `led_states.py` | State machine with stack-aware transitions |
| `led_hardware.py` | gpiozero GPIO abstraction |
| `test_leds.py` | Quick wiring verification script |
| `pokeball-leds.service` | systemd unit file |
| `install.sh` | Automated installer |
