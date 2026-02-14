/**
 * HTTP client for the PokeBall LED Controller daemon.
 *
 * All requests are fire-and-forget: failures are logged but never
 * propagate to the caller. The agent must never crash because LEDs
 * are unreachable.
 */

const DEFAULT_URL = "http://127.0.0.1:8420";

export class LedClient {
  private baseUrl: string;

  constructor(baseUrl?: string) {
    this.baseUrl = baseUrl || DEFAULT_URL;
  }

  async setState(state: string): Promise<void> {
    try {
      await fetch(`${this.baseUrl}/state`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ state }),
        signal: AbortSignal.timeout(2000),
      });
    } catch (err: any) {
      console.warn(`[pokeball] LED state update failed: ${err.message}`);
    }
  }

  async heartbeat(): Promise<void> {
    try {
      await fetch(`${this.baseUrl}/heartbeat`, {
        method: "POST",
        signal: AbortSignal.timeout(2000),
      });
    } catch (err: any) {
      // Silent: watchdog on the daemon side handles disconnection
    }
  }

  async getStatus(): Promise<string | null> {
    try {
      const res = await fetch(`${this.baseUrl}/status`, {
        signal: AbortSignal.timeout(2000),
      });
      const data = (await res.json()) as { state: string };
      return data.state;
    } catch {
      return null;
    }
  }
}
