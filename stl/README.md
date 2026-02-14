# 3D Printing Guide

Five parts make up the PokeBall enclosure. Print them separately with the colors and settings below.

## Parts Overview

| Part | File | Color | Description |
|------|------|-------|-------------|
| Top Half | `top-half.stl` | **Red** | Upper shell of the PokeBall |
| Bottom Half | `bottom-half.stl` | **White** | Lower shell of the PokeBall |
| Center Band | `center-band.stl` | **Black** | Equator band that joins the two halves |
| Button | `button.stl` | **White or translucent** | Center button (LED shines through this) |
| Button Bezel | `button-bezel.stl` | **Dark gray or black** | Ring around the center button |

## Print Settings

| Setting | Value | Notes |
|---------|-------|-------|
| Layer Height | 0.2mm | Standard quality, good enough for the shell |
| Infill | 15% | 20% for center band (structural) |
| Supports | Yes | For top-half and bottom-half interior cavities |
| Walls | 3 perimeters | Strength without excess weight |
| Material | PLA | PETG also works, PLA is easiest |
| Nozzle | 0.4mm | Standard |

## Special Notes

- **Button**: If you can print in translucent/clear PLA, do it. The LED behind it will glow through beautifully. If not, white PLA works fine - the light still diffuses through at 100% infill.
- **Top Half**: The interior needs supports. Orient it with the dome facing up.
- **Bottom Half**: Orient dome facing down. You may want to drill a small hole in the back for USB-C power cable access.
- **Center Band**: No supports needed. This is the structural piece - use 20% infill.
- **Button Bezel**: Small part, prints fast. Press-fits around the button.

## Assembly Order

1. Print all five parts
2. Drill a hole in the bottom half for USB-C power cable
3. Optionally drill/enlarge the button hole if needed for LED fitment
4. Press-fit the button into the button bezel
5. Insert the button+bezel assembly into the center band
6. Snap/glue the top half onto the center band
7. Snap/glue the bottom half onto the center band
8. The Pi and LEDs go inside before closing (see [hardware/assembly-guide.md](../hardware/assembly-guide.md))

## Estimated Print Times

| Part | Time | Filament |
|------|------|----------|
| Top Half | ~3 hours | ~30g |
| Bottom Half | ~3 hours | ~35g |
| Center Band | ~1.5 hours | ~15g |
| Button | ~15 min | ~2g |
| Button Bezel | ~20 min | ~3g |
| **Total** | **~8 hours** | **~85g** |
