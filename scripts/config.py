"""
Noti-Bot Configuration
======================
Edit this file with your specific IDs and channels.
"""

# OpenClaw bot user ID (the bot you want to trigger)
# Find this in Discord: Right-click the bot > Copy User ID
OPENCLAW_BOT_ID = 1234567890123456789  # <-- CHANGE THIS

# Channels to watch for reactions
# Find channel IDs: Right-click channel > Copy Channel ID
WATCHED_CHANNELS = [
    1234567890123456789,  # #example-channel  <-- CHANGE THIS
]

# Emoji to selection mapping
# Format: 'emoji': ('code', 'display_name')
EMOJI_MAP = {
    '1️⃣': ('1', '1번'), '1⃣': ('1', '1번'),
    '2️⃣': ('2', '2번'), '2⃣': ('2', '2번'),
    '3️⃣': ('3', '3번'), '3⃣': ('3', '3번'),
    '4️⃣': ('4', '4번'), '4⃣': ('4', '4번'),
    '5️⃣': ('5', '5번'), '5⃣': ('5', '5번'),
    '6️⃣': ('6', '6번'), '6⃣': ('6', '6번'),
    '7️⃣': ('7', '7번'), '7⃣': ('7', '7번'),
    '8️⃣': ('8', '8번'), '8⃣': ('8', '8번'),
    '9️⃣': ('9', '9번'), '9⃣': ('9', '9번'),
    '0️⃣': ('10', '10번'), '0⃣': ('10', '10번'),
    '✅': ('yes', '승인'),
    '❌': ('no', '거절'),
}
