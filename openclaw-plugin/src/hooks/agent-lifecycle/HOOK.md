---
name: pokeball-agent-lifecycle
description: Sends LED state updates when agent starts/ends processing
events:
  - before_agent_start
  - agent_end
enabled: true
---

# PokeBall Agent Lifecycle Hook

Updates the PokeBall LEDs when the OpenClaw agent begins or finishes
processing a user message.

- `before_agent_start` -> Blue LED (thinking)
- `agent_end` (success) -> Green flash
- `agent_end` (error) -> Red blink
