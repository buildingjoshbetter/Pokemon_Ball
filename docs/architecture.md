# Architecture

Technical deep-dive into how the PokeBall OpenClaw rig works.

## System Overview

```
┌─────────────┐         ┌──────────────────────────────────────┐
│  Your Phone  │         │         RASPBERRY PI 5 (PokeBall)    │
│  (Telegram)  │◄───────►│                                      │
└─────────────┘         │  ┌──────────────────────────────┐    │
                        │  │     OpenClaw Gateway          │    │
                        │  │     (Node.js)                 │    │
                        │  │                               │    │
                        │  │  ┌─────────────────────────┐  │    │
                        │  │  │  pokeball-led plugin     │  │    │
                        │  │  │                          │  │    │
                        │  │  │  Hooks:                  │  │    │
                        │  │  │   before_agent_start     │──┼──┐ │
                        │  │  │   agent_end              │  │  │ │
                        │  │  │   before_tool_call       │  │  │ │
                        │  │  │   after_tool_call        │  │  │ │
                        │  │  │                          │  │  │ │
                        │  │  │  Service:                │  │  │ │
                        │  │  │   heartbeat (5s)         │──┼──┤ │
                        │  │  └─────────────────────────┘  │  │ │
                        │  └──────────────────────────────┘  │ │
                        │                                     │ │
                        │  HTTP POST to 127.0.0.1:8420       │ │
                        │                                     │ │
                        │  ┌──────────────────────────────┐  │ │
                        │  │   LED Controller Daemon       │◄─┘ │
                        │  │   (Python / FastAPI)          │    │
                        │  │                               │    │
                        │  │   State Machine (stack-aware)  │    │
                        │  │          │                    │    │
                        │  │          ▼                    │    │
                        │  │   gpiozero GPIO control       │    │
                        │  │     │       │       │         │    │
                        │  └─────┼───────┼───────┼─────────┘    │
                        │        │       │       │              │
                        │     [RED]   [GREEN]  [BLUE]           │
                        │     GPIO22  GPIO27   GPIO17           │
                        └──────────────────────────────────────┘
```

## Communication Flow

1. **User sends Telegram message** to the bot
2. **OpenClaw Gateway** receives the message via Telegram channel
3. **`before_agent_start` hook fires** → plugin POSTs `{"state": "agent_active"}` to LED daemon
4. **LED daemon** transitions state machine → blue LED turns on solid
5. **Agent calls a tool** → `before_tool_call` hook → blue LED starts blinking fast
6. **Tool returns** → `after_tool_call` hook → blue LED back to solid
7. **Agent finishes** → `agent_end` hook → green LED flashes (success) or red blinks (error)
8. **Auto-transition** → back to green pulse (idle)

## State Machine

```
                    ┌─────────┐
             ┌──────│  BOOT   │
             │      └────┬────┘
             │           │ heartbeat received
             │      ┌────▼────┐
             │  ┌──►│  IDLE   │◄──────────────┐
             │  │   └────┬────┘               │
             │  │        │ before_agent_start  │ auto (500ms)
             │  │   ┌────▼─────────┐    ┌─────┴─────┐
             │  │   │ AGENT_ACTIVE │───►│  SUCCESS   │
             │  │   └────┬────┬────┘    └───────────┘
             │  │        │    │
             │  │        │    │ agent_end (error)
             │  │        │    │         ┌───────┐
             │  │        │    └────────►│ ERROR │
             │  │        │              └───────┘
             │  │        │ before_tool_call
             │  │   ┌────▼────┐
             │  │   │TOOL_CALL│──► after_tool_call ──► AGENT_ACTIVE
             │  │   └─────────┘                        (pop stack)
             │  │
             │  │  heartbeat timeout (15s)
             │  │   ┌──────────────┐
             │  └───│ DISCONNECTED │
             │      └──────────────┘
             │           │ heartbeat resumed
             └───────────┘
```

### Stack-Aware Transitions

The state machine uses a stack (not a simple variable) to handle nested events:

- `TOOL_CALL` **pushes** onto the stack
- `after_tool_call` **pops** back to `AGENT_ACTIVE`
- Terminal states (`IDLE`, `SUCCESS`, `ERROR`) **collapse** the entire stack

This prevents a bug where ending a tool call would jump straight to `IDLE` instead of returning to `AGENT_ACTIVE`.

## Heartbeat Watchdog

The plugin sends a heartbeat POST every 5 seconds. The LED daemon runs a watchdog thread that checks:

- If no heartbeat received for 15 seconds → transition to `DISCONNECTED`
- When heartbeat resumes → transition back to `IDLE`

This handles gateway crashes, network issues, or the OpenClaw process being stopped.

## Error Handling

The plugin uses **fire-and-forget** semantics:
- Every HTTP call to the LED daemon is wrapped in try/catch
- Failures are logged as warnings, never thrown
- The agent continues working normally even if LEDs are unreachable
- The LED daemon is a **nice-to-have**, not a dependency

## Port and Security

- LED daemon binds to `127.0.0.1:8420` (localhost only)
- Not exposed to the network
- No authentication needed (only local processes can reach it)
