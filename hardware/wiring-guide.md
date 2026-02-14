# Wiring Guide

Three LEDs connect to the Raspberry Pi's GPIO header. That's it - 4 wires total.

## GPIO Pin Mapping

| LED | GPIO Pin | Physical Pin | Resistor |
|-----|----------|-------------|----------|
| Blue | GPIO 17 | Pin 11 | 330Ω |
| Green | GPIO 27 | Pin 13 | 330Ω |
| Red | GPIO 22 | Pin 15 | 330Ω |
| Ground (shared) | GND | Pin 9 | - |

## Wiring Diagram

```
Raspberry Pi GPIO Header (pins 1-20 shown)
┌─────────────────────────────┐
│  (3.3V) 1  ●  ● 2  (5V)    │
│  (SDA)  3  ●  ● 4  (5V)    │
│  (SCL)  5  ●  ● 6  (GND)   │
│         7  ●  ● 8          │
│  (GND)  9  ●──● 10         │
│ (GP17) 11  ●  ● 12         │  ← GPIO 17 = Blue LED
│ (GP27) 13  ●  ● 14  (GND)  │  ← GPIO 27 = Green LED
│ (GP22) 15  ●  ● 16         │  ← GPIO 22 = Red LED
│  (3.3V)17  ●  ● 18         │
│        19  ●  ● 20  (GND)  │
└─────────────────────────────┘

Wiring for each LED:

  GPIO Pin ──→ 330Ω Resistor ──→ LED (+ long leg) ──→ LED (- short leg) ──→ GND

All three LEDs share one GND connection (Pin 9).
```

## Step-by-Step

1. **Connect the ground wire.** Run a jumper wire from **Pin 9 (GND)** to a common ground point (breadboard ground rail, or solder all LED ground legs together).

2. **Wire the Blue LED.**
   - GPIO 17 (Pin 11) → 330Ω resistor → Blue LED anode (+, long leg)
   - Blue LED cathode (-, short leg) → GND

3. **Wire the Green LED.**
   - GPIO 27 (Pin 13) → 330Ω resistor → Green LED anode (+, long leg)
   - Green LED cathode (-, short leg) → GND

4. **Wire the Red LED.**
   - GPIO 22 (Pin 15) → 330Ω resistor → Red LED anode (+, long leg)
   - Red LED cathode (-, short leg) → GND

## LED Placement

Position all three LEDs behind the PokeBall's center button. The translucent/white button acts as a diffuser, blending the colors:

```
        ┌──────────────┐
        │   PokeBall   │
        │   Button     │
        │  (diffuser)  │
        ├──────────────┤
        │  🔴 🟢 🔵   │  ← LEDs pointing at button
        │  (R) (G) (B) │
        │              │
        │  [  Pi 5  ]  │
        └──────────────┘
```

Hot glue the LEDs in place pointing toward the button. Leave enough wire length to open the PokeBall if needed.

## Verification

After wiring, run the test script:

```bash
cd /opt/pokeball-openclaw/led-controller
python3 test_leds.py
```

This cycles through each LED individually, then demos all states.
