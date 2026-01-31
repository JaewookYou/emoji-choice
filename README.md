# Noti-Bot: Reaction Forwarder

Discord reaction을 감지하여 메시지로 전달하는 봇.
OpenClaw가 reaction을 직접 턴 트리거로 인식하지 못하는 문제를 해결.

## 설정

1. Discord Developer Portal에서 봇의 **Privileged Gateway Intents** 활성화:
   - ✅ Message Content Intent
   - ✅ Server Members Intent

2. `.env` 파일에 토큰 설정 (이미 설정됨)

## 실행

```bash
cd ~/.openclaw/workspace/bots/noti-bot
pip install -r requirements.txt
python bot.py
```

## 백그라운드 실행

```bash
# tmux 사용
tmux new-session -d -s noti-bot "cd ~/.openclaw/workspace/bots/noti-bot && python bot.py"

# 또는 nohup
nohup python bot.py > noti-bot.log 2>&1 &
```

## 동작 방식

1. OpenClaw 봇이 이모지 선택 메시지 전송
2. 유저가 이모지 클릭
3. Noti-Bot이 reaction 감지
4. Noti-Bot이 "[선택] N번을 선택했습니다" 메시지 전송
5. OpenClaw가 이 메시지를 보고 해당 선택 처리
