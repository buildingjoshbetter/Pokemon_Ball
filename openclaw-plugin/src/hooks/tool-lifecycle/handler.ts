/**
 * Tool lifecycle hook for PokeBall LEDs.
 *
 * Maps tool call events to LED states:
 *   before_tool_call -> tool_call (blue fast blink)
 *   after_tool_call  -> agent_active (blue solid, pop stack)
 */

import { LedClient } from "../../led-client";

const ledClient = new LedClient();

export default async function handler(event: any): Promise<void> {
  try {
    if (event.hook === "before_tool_call") {
      await ledClient.setState("tool_call");
    } else if (event.hook === "after_tool_call") {
      await ledClient.setState("agent_active");
    }
  } catch (err: any) {
    // Fire-and-forget: never crash the agent for LED failures
    console.warn(`[pokeball] tool-lifecycle hook failed: ${err.message}`);
  }
}
