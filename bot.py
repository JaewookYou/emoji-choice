#!/usr/bin/env python3
"""
Noti-Bot: Discord Reaction Forwarder for OpenClaw
==================================================
Detects Discord reactions and forwards them as messages to OpenClaw.

Usage:
    python bot.py

Environment:
    DISCORD_BOT_TOKEN: Your Noti-Bot Discord token (not OpenClaw's token)
"""

import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load config
from config import OPENCLAW_BOT_ID, WATCHED_CHANNELS, EMOJI_MAP

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
BOT_ID = None


@bot.event
async def on_ready():
    global BOT_ID
    BOT_ID = bot.user.id
    logger.info(f"🤖 Noti-Bot started: {bot.user.name} (ID: {BOT_ID})")
    logger.info(f"📡 Watching channels: {WATCHED_CHANNELS}")
    logger.info(f"🎯 OpenClaw bot ID: {OPENCLAW_BOT_ID}")


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    """Handle reaction add events"""
    global BOT_ID
    
    # Ignore own reactions
    if payload.user_id == BOT_ID:
        return
    
    # Ignore OpenClaw bot reactions (initial emoji setup)
    if payload.user_id == OPENCLAW_BOT_ID:
        return
    
    # Filter by watched channels
    if WATCHED_CHANNELS and payload.channel_id not in WATCHED_CHANNELS:
        return
    
    emoji_str = str(payload.emoji)
    emoji_clean = emoji_str.replace('\ufe0f', '')
    
    # Check emoji mapping
    if emoji_str in EMOJI_MAP:
        selection = EMOJI_MAP[emoji_str]
    elif emoji_clean in EMOJI_MAP:
        selection = EMOJI_MAP[emoji_clean]
    else:
        return
    
    logger.info(f"🎯 Reaction detected: {emoji_str} → {selection[1]}")
    
    try:
        channel = bot.get_channel(payload.channel_id)
        if not channel:
            channel = await bot.fetch_channel(payload.channel_id)
        
        # Verify the message is from OpenClaw
        try:
            message = await channel.fetch_message(payload.message_id)
            if message.author.id != OPENCLAW_BOT_ID:
                logger.info("   ⏭️ Not an OpenClaw message, skipping")
                return
        except Exception as e:
            logger.warning(f"   ⚠️ Failed to verify message: {e}")
        
        # Get user info
        try:
            user = await bot.fetch_user(payload.user_id)
            user_name = user.display_name
        except:
            user_name = str(payload.user_id)
        
        # Forward to OpenClaw with mention
        forward_msg = f"<@{OPENCLAW_BOT_ID}> [Selection] {user_name} selected {selection[1]}."
        await channel.send(forward_msg)
        
        logger.info(f"✅ Forwarded: {forward_msg}")
        
    except Exception as e:
        logger.error(f"❌ Failed to send: {e}")


@bot.command(name="ping")
async def ping(ctx):
    """Check bot status"""
    await ctx.send("🏓 Pong! Noti-Bot is running!")


def main():
    if not DISCORD_TOKEN:
        logger.error("❌ DISCORD_BOT_TOKEN not set")
        logger.error("   Set it in .env file")
        return
    
    logger.info("🚀 Starting Noti-Bot...")
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
