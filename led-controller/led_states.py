"""
PokeBall LED State Machine

Stack-aware state machine that manages LED transitions based on
OpenClaw agent lifecycle events. The stack ensures nested events
(like tool calls inside an agent run) resolve correctly.
"""

from enum import Enum
from typing import Callable, Optional
import threading


class LedState(Enum):
    BOOT = "boot"
    IDLE = "idle"
    AGENT_ACTIVE = "agent_active"
    TOOL_CALL = "tool_call"
    SUCCESS = "success"
    ERROR = "error"
    DISCONNECTED = "disconnected"


# LED patterns: keyed by state
# "type" determines behavior:
#   solid   - constant on
#   blink   - on/off at interval
#   pulse   - smooth fade in/out at interval
#   cycle   - rotate through colors at interval
#   flash   - brief on, then auto-transition to "then" state
LED_PATTERNS = {
    LedState.BOOT: {
        "type": "cycle",
        "colors": ["red", "green", "blue"],
        "interval": 0.5,
    },
    LedState.IDLE: {
        "type": "pulse",
        "color": "green",
        "interval": 2.0,
    },
    LedState.AGENT_ACTIVE: {
        "type": "solid",
        "color": "blue",
    },
    LedState.TOOL_CALL: {
        "type": "blink",
        "color": "blue",
        "interval": 0.1,
    },
    LedState.SUCCESS: {
        "type": "flash",
        "color": "green",
        "duration": 0.5,
        "then": LedState.IDLE,
    },
    LedState.ERROR: {
        "type": "blink",
        "color": "red",
        "interval": 0.2,
    },
    LedState.DISCONNECTED: {
        "type": "pulse",
        "color": "red",
        "interval": 2.0,
    },
}


class StateMachine:
    """Stack-aware LED state machine.

    The stack handles nested events correctly:
    - TOOL_CALL pushes onto the stack
    - Ending a tool call pops back to AGENT_ACTIVE
    - Terminal states (IDLE, SUCCESS, ERROR) collapse the stack
    """

    def __init__(self, on_state_change: Callable[[LedState], None]):
        self._stack: list[LedState] = [LedState.BOOT]
        self._on_change = on_state_change
        self._lock = threading.Lock()

    @property
    def current(self) -> LedState:
        with self._lock:
            return self._stack[-1]

    def transition(self, new_state: LedState) -> LedState:
        with self._lock:
            old = self._stack[-1]

            if new_state == LedState.TOOL_CALL:
                # Push: tool call inside an agent run
                self._stack.append(new_state)
            elif new_state == LedState.AGENT_ACTIVE and old == LedState.TOOL_CALL:
                # Pop: tool call finished, return to agent active
                self._stack.pop()
            elif new_state in (
                LedState.IDLE,
                LedState.SUCCESS,
                LedState.ERROR,
                LedState.DISCONNECTED,
                LedState.BOOT,
            ):
                # Collapse: terminal states reset the stack
                self._stack = [new_state]
            else:
                # Replace top of stack
                self._stack[-1] = new_state

            current = self._stack[-1]

        # Notify outside the lock to avoid deadlocks
        self._on_change(current)
        return current
