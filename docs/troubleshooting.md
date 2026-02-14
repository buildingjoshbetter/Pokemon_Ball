# Troubleshooting

Common issues and fixes for the PokeBall OpenClaw rig.

## LEDs don't light up at all

**Check wiring polarity.** LEDs only work in one direction. The longer leg is positive (anode) and goes toward the GPIO pin (through the resistor). The shorter leg is negative (cathode) and goes to ground.

**Check GPIO pins.** Run `python3 test_leds.py` to test each LED individually. If no LEDs work, check that your ground wire is connected to Pin 9.

**Check the daemon is running:**
```bash
sudo systemctl status pokeball-leds
curl http://127.0.0.1:8420/status
```

## LEDs stay in BOOT (cycling R/G/B forever)

The LED daemon is running but hasn't received a heartbeat from OpenClaw. This means OpenClaw's gateway isn't running or the plugin isn't loaded.

**Fix:**
```bash
# Check OpenClaw is running
openclaw gateway status

# Check plugin is enabled
cat ~/.openclaw/openclaw.json | grep pokeball

# Restart gateway
openclaw gateway restart
```

## LEDs show DISCONNECTED (slow red pulse)

The LED daemon lost contact with the OpenClaw gateway (no heartbeat for 15+ seconds).

**Fix:**
```bash
# Check OpenClaw gateway
openclaw gateway status

# Check logs
journalctl -u pokeball-leds -f
```

## Telegram bot doesn't respond

**Check bot token:**
```bash
# Verify token is set in config
cat ~/.openclaw/openclaw.json | grep botToken
```

**Check pairing:**
```bash
# List paired users
openclaw channels status
```

**Common fix:** Make sure you messaged the bot first on Telegram to trigger the pairing flow, then approved the pairing code.

## LED daemon crashes on startup

**"Permission denied" for GPIO:**
```bash
# Add user to gpio group
sudo usermod -a -G gpio $USER
# Log out and back in, or reboot
```

**"Address already in use":**
```bash
# Something else is on port 8420
sudo lsof -i :8420
# Kill it or change the port in led_daemon.py
```

## Pi overheating inside the PokeBall

- Make sure the heatsink is attached to the CPU
- Don't seal the PokeBall airtight - small gaps provide airflow
- For heavy usage, leave the top half slightly open
- Check temperature: `vcgencmd measure_temp`

## Plugin hooks not firing

Check that the hooks are registered correctly:
```bash
openclaw hooks list
```

Make sure the plugin directory structure is correct:
```
~/.openclaw/plugins/pokeball-led/
├── dist/
│   ├── index.js
│   ├── led-client.js
│   └── hooks/
│       ├── agent-lifecycle/
│       │   └── handler.js
│       └── tool-lifecycle/
│           └── handler.js
└── package.json
```
