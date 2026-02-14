"""
PokeBall LED Hardware Abstraction

Wraps gpiozero for GPIO control. On non-Pi hardware (dev/testing),
gpiozero automatically falls back to a mock pin factory.
"""

import threading
import time
from typing import Optional

try:
    from gpiozero import LED, PWMLED
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False


class LedController:
    """Controls three LEDs (red, green, blue) on GPIO pins."""

    def __init__(self, red_pin: int = 22, green_pin: int = 27, blue_pin: int = 17):
        self._animation_stop = threading.Event()
        self._animation_thread: Optional[threading.Thread] = None

        if GPIO_AVAILABLE:
            # PWMLED supports brightness control for pulse/fade effects
            self.red = PWMLED(red_pin)
            self.green = PWMLED(green_pin)
            self.blue = PWMLED(blue_pin)
            self._leds = {"red": self.red, "green": self.green, "blue": self.blue}
        else:
            self.red = None
            self.green = None
            self.blue = None
            self._leds = {}
            print("[LED] GPIO not available - running in mock mode")

    def all_off(self):
        """Turn all LEDs off and stop any animation."""
        self._stop_animation()
        for led in self._leds.values():
            if led:
                led.off()

    def apply_pattern(self, pattern: dict):
        """Apply an LED pattern from LED_PATTERNS."""
        self._stop_animation()

        ptype = pattern["type"]

        if ptype == "solid":
            self._solid(pattern["color"])
        elif ptype == "blink":
            self._start_animation(self._blink, pattern["color"], pattern["interval"])
        elif ptype == "pulse":
            self._start_animation(self._pulse, pattern["color"], pattern["interval"])
        elif ptype == "cycle":
            self._start_animation(self._cycle, pattern["colors"], pattern["interval"])
        elif ptype == "flash":
            self._start_animation(
                self._flash, pattern["color"], pattern["duration"], pattern.get("then")
            )

    def _solid(self, color: str):
        """Turn on a single LED at full brightness."""
        self.all_off()
        led = self._leds.get(color)
        if led:
            led.value = 1.0

    def _blink(self, color: str, interval: float):
        """Blink a single LED on/off."""
        led = self._leds.get(color)
        if not led:
            return
        while not self._animation_stop.is_set():
            led.value = 1.0
            if self._animation_stop.wait(interval):
                break
            led.value = 0.0
            if self._animation_stop.wait(interval):
                break

    def _pulse(self, color: str, interval: float):
        """Smooth fade in/out (breathing effect)."""
        led = self._leds.get(color)
        if not led:
            return
        steps = 50
        step_time = interval / steps
        while not self._animation_stop.is_set():
            # Fade in
            for i in range(steps):
                if self._animation_stop.is_set():
                    return
                led.value = i / steps
                time.sleep(step_time)
            # Fade out
            for i in range(steps, 0, -1):
                if self._animation_stop.is_set():
                    return
                led.value = i / steps
                time.sleep(step_time)

    def _cycle(self, colors: list[str], interval: float):
        """Cycle through colors one at a time."""
        while not self._animation_stop.is_set():
            for color in colors:
                if self._animation_stop.is_set():
                    return
                for led in self._leds.values():
                    if led:
                        led.off()
                led = self._leds.get(color)
                if led:
                    led.value = 1.0
                if self._animation_stop.wait(interval):
                    return

    def _flash(self, color: str, duration: float, then_state=None):
        """Brief flash, then return to callback state."""
        led = self._leds.get(color)
        if led:
            led.value = 1.0
        self._animation_stop.wait(duration)
        if led:
            led.off()
        # The "then" transition is handled by the state machine via auto-transition

    def _start_animation(self, func, *args):
        """Start an animation in a background thread."""
        self._animation_stop.clear()
        self._animation_thread = threading.Thread(
            target=func, args=args, daemon=True
        )
        self._animation_thread.start()

    def _stop_animation(self):
        """Stop any running animation."""
        self._animation_stop.set()
        if self._animation_thread and self._animation_thread.is_alive():
            self._animation_thread.join(timeout=1.0)
        self._animation_thread = None

    def cleanup(self):
        """Clean up GPIO resources."""
        self.all_off()
        for led in self._leds.values():
            if led:
                led.close()
