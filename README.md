# Emoji Choice

Discord reaction-based selection handler for [OpenClaw](https://github.com/openclaw/openclaw).

Bridges the gap between Discord reactions and OpenClaw agent turns by forwarding emoji selections as messages.

## 🎯 Problem

OpenClaw receives Discord reaction events as system messages, but these don't trigger agent turns. Users clicking emoji buttons get no response.

## ✨ Solution

Emoji Choice bot detects reactions and forwards them as regular messages that mention OpenClaw, triggering a proper agent turn.

```
User clicks 2️⃣ → Emoji Choice detects → "@OpenClaw [Selection] user chose option 2" → OpenClaw responds
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- A separate Discord bot token (not your OpenClaw token)
- OpenClaw with `allowBots: true` in config

### Installation

```bash
git clone https://github.com/yourusername/emoji-choice.git
cd emoji-choice
pip install -r requirements.txt
cp .env.example .env
```

### Configuration

1. **Edit `.env`** with your bot token:
```bash
DISCORD_BOT_TOKEN=your_emoji_choice_bot_token
```

2. **Edit `config.py`** with your IDs:
```python
OPENCLAW_BOT_ID = 1234567890123456789  # Your OpenClaw bot
WATCHED_CHANNELS = [1234567890123456789]  # Channels to monitor
```

3. **Discord Developer Portal** → Bot → Enable:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent

4. **OpenClaw config** (`~/.openclaw/openclaw.json`):
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

### Run

```bash
python bot.py
```

Background mode:
```bash
nohup python bot.py > bot.log 2>&1 &
```

## 📋 Emoji Mapping

| Emoji | Selection | Use Case |
|-------|-----------|----------|
| 1️⃣~9️⃣ | 1~9 | Multiple choice |
| 0️⃣ | 10 | Multiple choice |
| ✅ | yes | Approve/Confirm |
| ❌ | no | Reject/Cancel |

## 🔄 Example Workflow

```
[OpenClaw]
Choose a recipe:
1️⃣ Kimchi Stew
2️⃣ Soybean Paste Stew
3️⃣ Tofu Stew

[User clicks 2️⃣]

[Emoji Choice]
@OpenClaw [Selection] user selected option 2.

[OpenClaw]
You chose Soybean Paste Stew! Starting...
```

## 📁 Files

```
emoji-choice/
├── bot.py              # Main bot
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── .env.example        # Environment template
├── .gitignore
├── README.md           # English docs
└── README.ko.md        # Korean docs
```

## ⚠️ Notes

- **Separate token required**: Use a different bot token from OpenClaw
- **Single instance**: Run only one instance to avoid duplicates
- **OpenClaw messages only**: Only reacts to emoji on OpenClaw's messages

## 📝 License

MIT License

---

[한국어 문서](README.ko.md)
