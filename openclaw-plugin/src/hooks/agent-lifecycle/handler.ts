/**
 * Agent lifecycle hook for PokeBall LEDs.
 *
 * Maps agent start/end events to LED states:
 *   before_agent_start -> agent_active (blue solid)
 *   agent_end (ok)     -> success (green flash)
 *   agent_end (error)  -> error (red blink)
 */

import { LedClient } from "../../led-client";

const ledClient = new LedClient();

export default async function handler(event: any): Promise<void> {
  try {
    if (event.hook === "before_agent_start") {
      await ledClient.setState("agent_active");
    } else if (event.hook === "agent_end") {
      const hasError = event.context?.error != null;
      await ledClient.setState(hasError ? "error" : "success");
    }
  } catch (err: any) {
    // Fire-and-forget: never crash the agent for LED failures
    console.warn(`[pokeball] agent-lifecycle hook failed: ${err.message}`);
  }
}
