/**
 * PokeBall LED Plugin for OpenClaw
 *
 * Bridges the OpenClaw agent lifecycle to a physical PokeBall
 * with LED indicators. Registers lifecycle hooks and a background
 * heartbeat service.
 *
 * Architecture:
 *   OpenClaw hooks -> this plugin -> HTTP -> LED daemon -> GPIO -> LEDs
 */

import { LedClient } from "./led-client";

const LED_DAEMON_URL = process.env.POKEBALL_LED_URL || "http://127.0.0.1:8420";
const HEARTBEAT_INTERVAL = 5000; // 5 seconds

export default function (api: any) {
  const ledClient = new LedClient(LED_DAEMON_URL);

  // Register the heartbeat background service
  api.registerService({
    id: "pokeball-heartbeat",

    start: async () => {
      api.logger.info("[pokeball] Heartbeat service started");

      // Gateway is up: transition from BOOT to IDLE
      await ledClient.setState("idle");

      const interval = setInterval(() => {
        ledClient.heartbeat().catch((err: Error) => {
          api.logger.warn(`[pokeball] Heartbeat failed: ${err.message}`);
        });
      }, HEARTBEAT_INTERVAL);

      // Return cleanup function
      return () => {
        clearInterval(interval);
      };
    },

    stop: async () => {
      api.logger.info("[pokeball] Heartbeat service stopping");
      await ledClient.setState("disconnected");
    },
  });

  // Expose ledClient to hooks via api context
  api.pokeball = { ledClient };
}
