#!/usr/bin/env python3
"""
Quick LED test script.

Run this directly on the Raspberry Pi to verify your wiring is correct.
It cycles through each LED individually, then runs through all states.

Usage:
    python3 test_leds.py
"""

import time

from led_hardware import LedController
from led_states import LED_PATTERNS, LedState

print("=== PokeBall LED Test ===\n")

hw = LedController(red_pin=22, green_pin=27, blue_pin=17)

# Test individual LEDs
for name, color in [("Red (GPIO 22)", "red"), ("Green (GPIO 27)", "green"), ("Blue (GPIO 17)", "blue")]:
    print(f"Testing {name}...")
    hw.all_off()
    led = hw._leds.get(color)
    if led:
        led.value = 1.0
    time.sleep(1.5)
    hw.all_off()
    time.sleep(0.5)

print("\n--- State Demos ---\n")

# Demo each state
for state in LedState:
    pattern = LED_PATTERNS[state]
    print(f"  {state.value:15s} -> {pattern['type']} ({pattern.get('color', pattern.get('colors', ''))})")
    hw.apply_pattern(pattern)
    time.sleep(3)
    hw.all_off()
    time.sleep(0.3)

hw.cleanup()
print("\nAll tests complete. If you saw each LED light up, wiring is correct.")
