<p align="center">
  <img src="assets/pokeball-logo.svg" alt="PokeBall OpenClaw" width="120" />
</p>

<h1 align="center">PokeBall OpenClaw</h1>

<p align="center">
  <strong>Your AI agent, captured.</strong><br>
  A living PokeBall that thinks, glows, and talks back.
</p>

<p align="center">
  <a href="#installation">Install</a> · <a href="#what-it-does">What It Does</a> · <a href="#why">Why</a> · <a href="#demo">Demo</a>
</p>

---

## What It Does

PokeBall OpenClaw is a 3D-printed PokeBall with a Raspberry Pi 5 inside, running [OpenClaw](https://openclaw.ai) — the open-source AI agent. You talk to it through Telegram. It thinks using Claude, GPT, or whatever LLM you point it at. And while it works, the center button glows to tell you what's happening.

Blue means it's thinking. Green means it answered. Red means something broke. When nobody's talking to it, it breathes — a slow green pulse, like it's sleeping inside the ball, waiting.

It's not a toy. It's a fully functional AI assistant that happens to live inside the most iconic capture device in fiction.

### Features

- **LED state engine** — A stack-aware state machine drives three LEDs through the PokeBall's translucent button. Seven distinct states: boot, idle, thinking, tool call, success, error, disconnected. The transitions are instantaneous — you see the ball react the moment you hit send.
- **Heartbeat watchdog** — The OpenClaw plugin pings the LED daemon every 5 seconds. If the gateway crashes, the ball knows. Slow red pulse. No false positives, no polling logs, no fragile workarounds.
- **Fire-and-forget architecture** — The LED system never interferes with the agent. Every call from the plugin to the daemon is wrapped in try/catch. If the LEDs die, the agent keeps working. Nice-to-have, not a dependency.
- **Telegram-native** — Designed for Telegram via OpenClaw's built-in channel. Message the bot, watch the ball, get your answer. No app, no dashboard, no browser tab.
- **Fully reproducible** — Five STL files, three LEDs, three resistors, one Pi. Every file you need is in this repo. Print it, wire it, run one script, you're live.
- **Always on** — systemd service starts the LED daemon on boot. Power cycle the Pi and everything comes back automatically. Hackathon-grade reliability.

## Installation

### Prerequisites

- [OpenClaw](https://github.com/openclaw/openclaw) installed and configured
- Telegram bot set up in OpenClaw (create one via [@BotFather](https://t.me/BotFather))
- Raspberry Pi 5 (8GB recommended) or Pi 4 (4GB minimum)
- 3D-printed PokeBall shell ([STL files included](stl/))

### Quick Install

1. Clone this repo onto your Pi:
```bash
git clone https://github.com/buildingjoshbetter/Pokemon_Ball.git
cd Pokemon_Ball
```

2. Run the setup script:
```bash
chmod +x scripts/setup-pi.sh
./scripts/setup-pi.sh
```

3. Add your Telegram bot token to `~/.openclaw/openclaw.json`:
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

4. Restart OpenClaw:
```bash
openclaw gateway restart
```

5. Message your bot on Telegram. Watch the ball glow. That's it.

### Hardware Setup

Three LEDs, three resistors, one ground wire:

```
GPIO 17 (Pin 11) ──► 330Ω ──► Blue LED  ──► GND (Pin 9)
GPIO 27 (Pin 13) ──► 330Ω ──► Green LED ──► GND (Pin 9)
GPIO 22 (Pin 15) ──► 330Ω ──► Red LED   ──► GND (Pin 9)
```

Position all three behind the center button. The translucent plastic acts as a diffuser.

Full guides: [Wiring](hardware/wiring-guide.md) · [Assembly](hardware/assembly-guide.md) · [Parts List](hardware/parts-list.md) · [3D Printing](stl/README.md)

## Demo

Send a message. Watch the ball.

```
You: What's the weather in Austin today?

[PokeBall: 🟢 green pulse → 🔵 solid blue]

Agent: Currently 72°F and sunny in Austin, TX. High of 78°F expected
       this afternoon with clear skies through the evening.

[PokeBall: 🔵 blue → 🟢 green flash → 🟢 green pulse]
```

Ask something that requires tools — the ball blinks faster:

```
You: Search the web for the latest OpenClaw release notes

[PokeBall: 🟢 → 🔵 solid blue → 🔵 fast blink (tool call)]

Agent: OpenClaw 2026.2.12 was released today with patches for 40+
       security vulnerabilities. Key changes include...

[PokeBall: 🔵 fast blink → 🔵 solid → 🟢 flash → 🟢 pulse]
```

If something goes wrong, you know immediately:

```
You: Connect to my database and run the migration

[PokeBall: 🟢 → 🔵 solid → 🔴 fast blink]

Agent: Connection refused on port 5432. Is PostgreSQL running?

[PokeBall: 🔴 blink for 3s → 🟢 pulse]
```

Kill the OpenClaw gateway and the ball tells you:

```
$ openclaw gateway stop

[PokeBall: ... 15 seconds pass ... 🔴 slow pulse (breathing)]
[The ball knows. It's waiting for its trainer to come back.]

$ openclaw gateway start

[PokeBall: 🔴 slow pulse → 🟢 pulse]
[Back online. Ready.]
```

Run the full demo without Telegram:

```bash
bash scripts/demo-sequence.sh
```

## Why

I was sitting at a hackathon staring at a terminal. Everyone around me had the same thing — a laptop, a code editor, an agent running in a window somewhere. You couldn't tell who was running what. You couldn't tell if anything was happening. The AI was invisible.

And I thought: that's the problem with agents. Not just at hackathons — everywhere. You fire off a request and then you sit there. Is it thinking? Did it crash? Is it stuck in a loop? You check the terminal. You check the logs. You wait. The most powerful technology we've ever built, and it has the presence of a loading spinner.

I had a 3D printer. I had a Raspberry Pi. I had a PokeBall model I'd been meaning to print for two years. And I had OpenClaw, an open-source agent that runs on a Pi and talks through Telegram.

So I caught one.

Three LEDs behind the button. A Python daemon listening on localhost. An OpenClaw plugin that fires on every lifecycle event. When the agent thinks, the ball glows blue. When it finishes, green flash. When it fails, red. When nobody's talking to it, it breathes — slow green pulse, like something alive is sleeping inside.

The moment I put it on the table, people walked over. Not because the code was impressive — it's straightforward. They walked over because they could *see* the AI. For the first time, the invisible thing had a body. It sat on the desk and it glowed and it breathed and when you talked to it, it reacted. That changes how you think about it. That changes how everyone around you thinks about it.

$105 in parts. An afternoon of work. Every file you need is in this repo.

Your move.

## Built By

**[@Building_Josh](https://x.com/Building_Josh)**

Built at a hackathon because AI agents deserve a body, and every trainer deserves a PokeBall on their desk.

## License

[MIT](LICENSE) — Gotta catch 'em all. Or at least this one.

---

<p align="center">
  <em>"I caught an AI."</em>
</p>

<p align="center">
  <img src="assets/pokeball-logo.svg" alt="PokeBall OpenClaw" width="40" />
</p>
