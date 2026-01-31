# Emoji Choice

[OpenClaw](https://github.com/openclaw/openclaw)를 위한 Discord 리액션 기반 선택 처리기.

이모지 선택을 메시지로 변환하여 OpenClaw 에이전트 턴을 트리거합니다.

## 🎯 문제

OpenClaw는 Discord reaction 이벤트를 시스템 메시지로 받지만, 에이전트 턴을 트리거하지 않습니다. 사용자가 이모지를 눌러도 응답이 없어요.

## ✨ 해결책

Emoji Choice 봇이 reaction을 감지하고, OpenClaw를 멘션하는 일반 메시지로 전달합니다.

```
사용자가 2️⃣ 클릭 → Emoji Choice 감지 → "@OpenClaw [선택] 2번을 선택했습니다" → OpenClaw 응답
```

## 🚀 빠른 시작

### 요구사항

- Python 3.8+
- 별도의 Discord 봇 토큰 (OpenClaw 토큰과 다른 것)
- OpenClaw 설정에 `allowBots: true`

### 설치

```bash
git clone https://github.com/yourusername/emoji-choice.git
cd emoji-choice
pip install -r requirements.txt
cp .env.example .env
```

### 설정

1. **`.env` 편집** - 봇 토큰 입력:
```bash
DISCORD_BOT_TOKEN=your_emoji_choice_bot_token
```

2. **`config.py` 편집** - ID 설정:
```python
OPENCLAW_BOT_ID = 1234567890123456789  # OpenClaw 봇 ID
WATCHED_CHANNELS = [1234567890123456789]  # 감시할 채널
```

3. **Discord Developer Portal** → Bot → 활성화:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent

4. **OpenClaw 설정** (`~/.openclaw/openclaw.json`):
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

### 실행

```bash
python bot.py
```

백그라운드 실행:
```bash
nohup python bot.py > bot.log 2>&1 &
```

## 📋 이모지 매핑

| 이모지 | 선택 | 용도 |
|--------|------|------|
| 1️⃣~9️⃣ | 1~9 | 다지선다 |
| 0️⃣ | 10 | 다지선다 |
| ✅ | yes | 승인/확인 |
| ❌ | no | 거절/취소 |

## 🔄 워크플로우 예시

```
[OpenClaw]
레시피를 선택하세요:
1️⃣ 김치찌개
2️⃣ 된장찌개
3️⃣ 순두부찌개

[사용자가 2️⃣ 클릭]

[Emoji Choice]
@OpenClaw [선택] arang님이 2번을 선택했습니다.

[OpenClaw]
된장찌개를 선택하셨네요! 진행할게요.
```

## 📁 파일 구조

```
emoji-choice/
├── bot.py              # 메인 봇
├── config.py           # 설정
├── requirements.txt    # 의존성
├── .env.example        # 환경변수 템플릿
├── .gitignore
├── README.md           # 영문 문서
└── README.ko.md        # 한글 문서
```

## ⚠️ 주의사항

- **별도 토큰 필요**: OpenClaw와 다른 봇 토큰 사용
- **단일 인스턴스**: 중복 메시지 방지를 위해 1개만 실행
- **OpenClaw 메시지만**: OpenClaw가 보낸 메시지의 reaction만 처리

## 📝 라이선스

MIT License

---

[English Documentation](README.md)
