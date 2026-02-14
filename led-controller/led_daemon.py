"""
PokeBall LED Controller Daemon

FastAPI server that receives state commands from the OpenClaw plugin
and drives GPIO LEDs on the Raspberry Pi.

Usage:
    uvicorn led_daemon:app --host 127.0.0.1 --port 8420
"""

import signal
import sys
import threading
import time

from fastapi import FastAPI
from pydantic import BaseModel

from led_hardware import LedController
from led_states import LED_PATTERNS, LedState, StateMachine

# --- Hardware ---
hardware = LedController(red_pin=22, green_pin=27, blue_pin=17)


def on_state_change(state: LedState):
    """Callback when state machine transitions."""
    pattern = LED_PATTERNS[state]
    hardware.apply_pattern(pattern)

    # Auto-transition for flash states
    if pattern["type"] == "flash" and pattern.get("then"):
        duration = pattern["duration"]
        then_state = pattern["then"]
        threading.Timer(duration, lambda: state_machine.transition(then_state)).start()


# --- State Machine ---
state_machine = StateMachine(on_state_change=on_state_change)

# --- Heartbeat Watchdog ---
last_heartbeat = time.time()
HEARTBEAT_TIMEOUT = 15.0  # seconds


def watchdog():
    """Transition to DISCONNECTED if heartbeat goes stale."""
    global last_heartbeat
    while True:
        time.sleep(5)
        elapsed = time.time() - last_heartbeat
        if elapsed > HEARTBEAT_TIMEOUT:
            current = state_machine.current
            if current not in (LedState.DISCONNECTED, LedState.BOOT):
                state_machine.transition(LedState.DISCONNECTED)


watchdog_thread = threading.Thread(target=watchdog, daemon=True)
watchdog_thread.start()

# --- API ---
app = FastAPI(
    title="PokeBall LED Controller",
    description="Controls LEDs inside the PokeBall based on OpenClaw agent state",
    version="1.0.0",
)


class StateRequest(BaseModel):
    state: str


class StateResponse(BaseModel):
    ok: bool
    state: str
    error: str | None = None


@app.put("/state", response_model=StateResponse)
def set_state(req: StateRequest):
    """Set the LED state. Called by the OpenClaw plugin."""
    try:
        new_state = LedState(req.state)
    except ValueError:
        valid = [s.value for s in LedState]
        return StateResponse(
            ok=False,
            state=state_machine.current.value,
            error=f"Unknown state '{req.state}'. Valid: {valid}",
        )

    result = state_machine.transition(new_state)
    return StateResponse(ok=True, state=result.value)


@app.post("/heartbeat", response_model=StateResponse)
def heartbeat():
    """Heartbeat from OpenClaw plugin. Resets watchdog timer."""
    global last_heartbeat
    last_heartbeat = time.time()

    if state_machine.current == LedState.DISCONNECTED:
        state_machine.transition(LedState.IDLE)

    return StateResponse(ok=True, state=state_machine.current.value)


@app.get("/status", response_model=StateResponse)
def status():
    """Get current LED state."""
    return StateResponse(ok=True, state=state_machine.current.value)


# --- Graceful Shutdown ---
def shutdown_handler(sig, frame):
    hardware.cleanup()
    sys.exit(0)


signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

# Start in BOOT state
on_state_change(LedState.BOOT)
