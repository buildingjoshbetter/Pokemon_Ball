<p align="center">
  <img src="logo.svg" width="200" alt="PokeBall OpenClaw Logo"/>
</p>

<h1 align="center">PokeBall OpenClaw</h1>

<p align="center">
  A 3D-printed PokeBall housing a Raspberry Pi 5 running <a href="https://github.com/openclaw/openclaw">OpenClaw</a> — an open-source AI agent you talk to through Telegram.<br/>
  The center button glows based on what the agent is doing.
</p>

<p align="center">
  <b>Your AI agent, captured.</b>
</p>

<p align="center">
  Built by <a href="https://x.com/Building_Josh">Building Josh</a> · MIT License
</p>

---

## What It Does

You send a message to a Telegram bot. Inside the PokeBall on your desk, a Raspberry Pi running OpenClaw processes your request — calling LLMs, running tools, searching the web — and sends back a response. The whole time, the PokeBall's center button tells you what's happening:

| State | Color | What's Happening |
|-------|-------|-----------------|
| Idle | Green pulse (breathing) | Waiting for a message |
| Thinking | Solid blue | Agent is processing your request |
| Tool call | Fast blue blink | Agent is running a tool (web search, file ops, etc.) |
| Success | Green flash | Response sent back to Telegram |
| Error | Red blink | Something went wrong |
| Disconnected | Slow red pulse | Gateway is down or unreachable |
| Boot | RGB cycle | Starting up |

## How It Works

Two programs run on the Pi, connected via HTTP on localhost:

```
[Your Phone]                    [PokeBall]
     │                               │
  Telegram ──► OpenClaw Gateway ──► pokeball-led plugin
                                         │
                                    HTTP POST
                                         │
                                    LED Daemon (Python)
                                         │
                                    GPIO ──► LEDs
```

1. **OpenClaw plugin** hooks into agent lifecycle events (`before_agent_start`, `agent_end`, `before_tool_call`, `after_tool_call`) and sends state changes to the LED daemon
2. **LED daemon** (Python/FastAPI) receives state commands and drives three LEDs via GPIO through a stack-aware state machine
3. A **heartbeat** every 5 seconds lets the LEDs detect if the gateway crashes

Full architecture details: [docs/architecture.md](docs/architecture.md)

## Parts List

| Part | Cost |
|------|------|
| Raspberry Pi 5 (8GB) | ~$80 |
| USB-C power supply (official) | ~$12 |
| MicroSD card (32GB+) | ~$10 |
| 3x LEDs (red, green, blue) | ~$0.30 |
| 3x 330 ohm resistors | ~$0.10 |
| Jumper wires | ~$0.50 |
| PLA filament (~85g) | ~$2 |
| **Total** | **~$105** |

Full parts list with links: [hardware/parts-list.md](hardware/parts-list.md)

## Quick Start

### 1. Print the PokeBall

Print the five STL files in the [`stl/`](stl/) directory:

| File | Color |
|------|-------|
| `top-half.stl` | Red |
| `bottom-half.stl` | White |
| `center-band.stl` | Black |
| `button.stl` | White or translucent |
| `button-bezel.stl` | Dark gray / black |

Print settings: 0.2mm layer height, 15% infill, PLA. See [stl/README.md](stl/README.md) for details.

### 2. Wire the LEDs

Three LEDs, three resistors, one ground wire. That's it.

```
GPIO 17 (Pin 11) ──► 330Ω ──► Blue LED  ──► GND (Pin 9)
GPIO 27 (Pin 13) ──► 330Ω ──► Green LED ──► GND (Pin 9)
GPIO 22 (Pin 15) ──► 330Ω ──► Red LED   ──► GND (Pin 9)
```

Full wiring guide: [hardware/wiring-guide.md](hardware/wiring-guide.md)

### 3. Assemble

Mount the Pi in the bottom half, position LEDs behind the button, route the USB-C cable out the back, close it up.

Full assembly guide: [hardware/assembly-guide.md](hardware/assembly-guide.md)

### 4. Install Software

Flash Raspberry Pi OS (64-bit Lite) to your SD card, then:

```bash
git clone https://github.com/YOUR_USERNAME/pokeball-openclaw.git
cd pokeball-openclaw
chmod +x scripts/setup-pi.sh
./scripts/setup-pi.sh
```

This installs Node.js 22, OpenClaw, the LED daemon, and the plugin.

### 5. Configure Telegram

1. Message [@BotFather](https://t.me/BotFather) on Telegram → `/newbot` → copy the token
2. Edit `~/.openclaw/openclaw.json`:

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "YOUR_BOT_TOKEN_HERE"
    }
  },
  plugins: {
    "pokeball-led": {
      enabled: true
    }
  }
}
```

3. Restart the gateway: `openclaw gateway restart`
4. Message your bot on Telegram and approve the pairing code

### 6. Test

```bash
# Test LED wiring
python3 /opt/pokeball-openclaw/led-controller/test_leds.py

# Test all states via API
bash scripts/test-leds.sh

# Run the full demo sequence
bash scripts/demo-sequence.sh
```

Send a message to your Telegram bot and watch the PokeBall glow.

## Project Structure

```
pokeball-openclaw/
├── stl/                    # 3D printable files + print guide
├── hardware/               # Wiring diagram, parts list, assembly guide
├── led-controller/         # Python LED daemon (runs on Pi)
├── openclaw-plugin/        # TypeScript plugin for OpenClaw
├── scripts/                # Setup and test scripts
└── docs/                   # Architecture + troubleshooting
```

## Troubleshooting

See [docs/troubleshooting.md](docs/troubleshooting.md) for common issues.

## License

MIT License. See [LICENSE](LICENSE).

Do whatever you want with this. Build one, modify it, make it better. If you do, tag [@Building_Josh](https://x.com/Building_Josh) — I'd love to see it.
