#!/bin/bash
# Emoji Choice Bot Startup Script
# Ensures only one instance is running

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$SCRIPT_DIR/bot.log"
PID_FILE="$SCRIPT_DIR/bot.pid"

cd "$SCRIPT_DIR" || exit 1

# Check if already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Emoji Choice already running (PID: $PID)"
        exit 0
    fi
fi

# Kill any orphan processes
pkill -f "emoji-choice.*bot.py" 2>/dev/null

# Start bot
nohup python3 bot.py > "$LOG_FILE" 2>&1 &
NEW_PID=$!
echo $NEW_PID > "$PID_FILE"

echo "Emoji Choice started (PID: $NEW_PID)"
