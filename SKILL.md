---
name: emoji-choice
description: Discord reaction-based selection handler for OpenClaw. Bridges the gap between Discord emoji reactions and agent turns by forwarding selections as triggering messages. Use when you need interactive emoji voting/selection on Discord (e.g., recipe selection, approval workflows, polls). Requires a separate Discord bot running alongside OpenClaw.
metadata:
  openclaw:
    emoji: "🎯"
    requires:
      bins: ["python3"]
    install:
      - id: pip
        kind: pip
        packages: ["discord.py>=2.0.0", "python-dotenv>=1.0.0"]
        label: "Install Python dependencies"
---

# Emoji Choice

Discord reaction-based selection handler that bridges emoji clicks to OpenClaw agent turns.

## Problem

OpenClaw receives Discord reaction events as system messages, but these don't trigger agent turns. Users clicking emoji get no response.

## Solution

Emoji Choice bot detects reactions and forwards them as regular messages mentioning OpenClaw, triggering a proper turn.

```
User clicks 2️⃣ → Bot detects → "@OpenClaw [Selection] chose 2" → OpenClaw responds
```

## Setup

### 1. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create new application → Bot section
3. Copy bot token
4. Enable Privileged Gateway Intents:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent

### 2. Configure Bot

Create `.env` in `scripts/`:
```bash
DISCORD_BOT_TOKEN=your_token_here
```

Edit `scripts/config.py`:
```python
OPENCLAW_BOT_ID = 1234567890  # Your OpenClaw bot ID
WATCHED_CHANNELS = [1234567890]  # Channel IDs to monitor
```

### 3. Configure OpenClaw

Add to `~/.openclaw/openclaw.json`:
```json
{
  "channels": {
    "discord": {
      "allowBots": true,
      "guilds": {
        "<guild_id>": {
          "channels": {
            "<channel_id>": {
              "allow": true,
              "users": ["<your_id>", "<emoji_choice_bot_id>"]
            }
          }
        }
      }
    }
  }
}
```

### 4. Run

```bash
python3 scripts/bot.py
```

Background:
```bash
nohup python3 scripts/bot.py > bot.log 2>&1 &
```

## Emoji Mapping

| Emoji | Selection |
|-------|-----------|
| 1️⃣~9️⃣ | 1~9 |
| 0️⃣ | 10 |
| ✅ | yes/approve |
| ❌ | no/reject |

## Workflow Example

```
[OpenClaw sends]
Choose a recipe:
1️⃣ Kimchi Stew
2️⃣ Soybean Stew

[User clicks 2️⃣]

[Emoji Choice sends]
@OpenClaw [Selection] user selected 2번.

[OpenClaw responds]
You chose Soybean Stew!
```

## Files

- `scripts/bot.py` - Main bot code
- `scripts/config.py` - Configuration template
- `scripts/start.sh` - Startup script with single-instance guard

## Notes

- **Separate bot token required** - Different from OpenClaw's token
- **Single instance** - Run only one instance to avoid duplicates
- **OpenClaw messages only** - Only processes reactions on OpenClaw's messages
