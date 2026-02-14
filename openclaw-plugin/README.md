# OpenClaw PokeBall LED Plugin

OpenClaw plugin that bridges agent lifecycle events to the PokeBall's LED indicators.

## How It Works

This plugin hooks into four OpenClaw lifecycle events:

| Event | LED State | Visual |
|-------|-----------|--------|
| `before_agent_start` | Agent Active | Solid blue |
| `before_tool_call` | Tool Call | Fast blue blink |
| `after_tool_call` | Agent Active | Back to solid blue |
| `agent_end` (success) | Success | Green flash |
| `agent_end` (error) | Error | Red blink |

It also runs a background heartbeat service that pings the LED daemon every 5 seconds. If the daemon stops receiving heartbeats (gateway crash), it transitions LEDs to a disconnected state (slow red pulse).

## Installation

### 1. Build the plugin

```bash
cd openclaw-plugin
npm install
npm run build
```

### 2. Copy to OpenClaw plugins directory

```bash
cp -r dist/ ~/.openclaw/plugins/pokeball-led/
cp package.json ~/.openclaw/plugins/pokeball-led/
```

### 3. Enable in OpenClaw config

Add to `~/.openclaw/openclaw.json`:

```json5
{
  plugins: {
    "pokeball-led": {
      enabled: true
    }
  }
}
```

### 4. Restart OpenClaw gateway

```bash
openclaw gateway restart
```

## Configuration

Set the `POKEBALL_LED_URL` environment variable to override the default LED daemon URL:

```bash
export POKEBALL_LED_URL="http://127.0.0.1:8420"
```

## Files

| File | Description |
|------|-------------|
| `src/index.ts` | Plugin entry: registers hooks + heartbeat service |
| `src/led-client.ts` | HTTP client for the LED daemon |
| `src/hooks/agent-lifecycle/` | Agent start/end hook |
| `src/hooks/tool-lifecycle/` | Tool call start/end hook |
