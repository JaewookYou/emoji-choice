#!/bin/bash
# Noti-Bot Startup Script
# Ensures only one instance is running

SCRIPT_DIR="$HOME/.openclaw/workspace/bots/noti-bot"
LOG_FILE="$SCRIPT_DIR/bot.log"
PID_FILE="$SCRIPT_DIR/bot.pid"

cd "$SCRIPT_DIR" || exit 1

# Check if already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Noti-Bot already running (PID: $PID)"
        exit 0
    fi
fi

# Kill any orphan processes
pkill -f "noti-bot/bot.py" 2>/dev/null

# Start bot
nohup python3 bot.py > "$LOG_FILE" 2>&1 &
NEW_PID=$!
echo $NEW_PID > "$PID_FILE"

echo "Noti-Bot started (PID: $NEW_PID)"
