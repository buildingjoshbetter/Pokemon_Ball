# Assembly Guide

How to put together the PokeBall OpenClaw rig. Total time: ~30 minutes (after printing).

## Before You Start

Make sure you have:
- All 5 printed parts (see [stl/README.md](../stl/README.md))
- Raspberry Pi 5 with OS installed and OpenClaw configured
- 3 LEDs wired to the Pi (see [wiring-guide.md](./wiring-guide.md))
- USB-C power cable
- Hot glue gun
- Small drill

## Assembly Steps

### 1. Prep the Bottom Half

Drill a hole in the back of the **bottom-half** piece for the USB-C power cable. Size it just large enough for the cable to pass through snugly.

Optionally drill a small hole nearby for HDMI if you want video output during demos.

### 2. Mount the Raspberry Pi

Place the Pi inside the bottom half. Use hot glue on the corners to secure it. Make sure:
- The USB-C power port aligns with the hole you drilled
- The GPIO pins face upward (toward where the button will be)
- There's room for the heatsink on top of the CPU

### 3. Attach the Heatsink

Stick the heatsink onto the Pi's CPU before closing. The PokeBall is semi-enclosed, so passive cooling helps.

### 4. Position the LEDs

Cluster the three LEDs together, pointing upward toward the center button hole. Hot glue them in place. The wires should be long enough to reach the GPIO pins with a little slack.

### 5. Assemble the Button

Press-fit the **button** piece into the **button-bezel** piece. This assembly sits in the center hole of the **center-band**.

### 6. Close It Up

1. Place the **center-band** onto the **bottom-half** (snap or glue)
2. Insert the **button+bezel** into the center-band's button hole
3. Route the USB-C cable out through the back hole
4. Place the **top-half** onto the center-band (snap or glue)

### 7. Final Check

- USB-C cable accessible from outside
- LEDs visible through the center button
- Pi powered on and accessible via SSH
- Run `python3 test_leds.py` to verify everything works

## Tips

- **Don't permanently glue the top half** until everything is tested. Use friction fit or small dabs of hot glue that can be broken if needed.
- **Cable management**: Coil excess LED wires inside. Use small cable ties if needed.
- **Ventilation**: The PokeBall doesn't need to be airtight. Small gaps between parts provide enough airflow for the Pi 5 with a heatsink.
- **Demo setup**: During your presentation, you can open the top half to show the internals. This is a great "reveal" moment.
