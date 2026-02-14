---
name: pokeball-tool-lifecycle
description: Sends LED state updates when tools are called during agent processing
events:
  - before_tool_call
  - after_tool_call
enabled: true
---

# PokeBall Tool Lifecycle Hook

Updates the PokeBall LEDs during tool execution:

- `before_tool_call` -> Fast blue blink (working)
- `after_tool_call` -> Back to solid blue (agent still thinking)
