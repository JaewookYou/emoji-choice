#!/usr/bin/env python3
"""
Noti-Bot: Reaction Forwarder
============================
Discord reaction을 감지하여 같은 채널에 메시지로 전달.
OpenClaw가 이 메시지를 보고 반응할 수 있게 함.

Usage:
    python bot.py
"""

import os
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

# 로컬 유틸리티 사용 (리포지토리 내부)
from utils.logger import get_logger

logger = get_logger("noti-bot")

load_dotenv()

# 설정
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")

# OpenClaw 봇 ID (이 봇이 보낸 메시지의 reaction만 처리)
OPENCLAW_BOT_ID = 1466835811201712289

# 감시할 채널 ID
WATCHED_CHANNELS = [
    1466837864502526066,  # #openclaw
    1467444367148060718,  # #twitter-choice (트위터)
    1467484477461889024,  # #recipe-choice (레시피)
    1467485025988513833,  # #misc-choice (기타/자가발전)
]

# 이모지 → 선택 매핑
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
    '🔥': ('all', '전체수행'),
}

# Discord 봇 설정
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 봇 자신의 ID (시작 시 설정)
BOT_ID = None


@bot.event
async def on_ready():
    global BOT_ID
    BOT_ID = bot.user.id
    logger.info(f"🤖 Noti-Bot 시작됨: {bot.user.name} (ID: {BOT_ID})")
    logger.info(f"📡 감시 채널: {WATCHED_CHANNELS}")
    logger.info(f"🎯 OpenClaw 봇 ID: {OPENCLAW_BOT_ID}")


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    """Reaction 추가 이벤트 처리"""
    global BOT_ID
    
    # 모든 reaction 로깅 (디버그)
    # logger.debug(f"🔔 [DEBUG] Reaction 수신: {payload.emoji} by {payload.user_id} on msg {payload.message_id}")
    
    # 자기 자신의 reaction은 무시
    if payload.user_id == BOT_ID:
        return
    
    # OpenClaw 봇의 reaction도 무시 (초기 이모지 추가)
    if payload.user_id == OPENCLAW_BOT_ID:
        return
    
    # 감시 채널 필터링
    if WATCHED_CHANNELS and payload.channel_id not in WATCHED_CHANNELS:
        return
    
    emoji_str = str(payload.emoji)
    
    # 이모지 정규화 (variation selector 제거)
    emoji_clean = emoji_str.replace('\ufe0f', '')
    
    # 매핑된 이모지만 처리
    if emoji_str in EMOJI_MAP:
        selection = EMOJI_MAP[emoji_str]
    elif emoji_clean in EMOJI_MAP:
        selection = EMOJI_MAP[emoji_clean]
    else:
        return  # 매핑에 없는 이모지는 무시
    
    logger.info(f"🎯 Reaction 감지: {emoji_str} → {selection[1]}")
    logger.info(f"   유저: {payload.user_id}, 채널: {payload.channel_id}, 메시지: {payload.message_id}")
    
    try:
        # 채널 가져오기
        channel = bot.get_channel(payload.channel_id)
        if not channel:
            channel = await bot.fetch_channel(payload.channel_id)
        
        # 원본 메시지 가져오기 (OpenClaw 봇이 보낸 건지 확인)
        try:
            message = await channel.fetch_message(payload.message_id)
            if message.author.id != OPENCLAW_BOT_ID:
                logger.info(f"   ⏭️ OpenClaw 메시지가 아님, 무시")
                return
        except Exception as e:
            logger.warning(f"   ⚠️ 메시지 확인 실패: {e}")
            # 확인 실패해도 일단 전달
        
        # 유저 정보 가져오기
        try:
            user = await bot.fetch_user(payload.user_id)
            user_name = user.display_name
        except:
            user_name = str(payload.user_id)
        
        # 선택된 옵션에 해당하는 내용 추출
        action_desc = ""
        try:
            lines = message.content.split('\n')
            selected_num = selection[0]  # '1', '2', 'all', 'yes', 'no' 등
            
            # 숫자 이모지 매핑
            number_emojis = {
                '1': ['1️⃣', '1⃣'], '2': ['2️⃣', '2⃣'], '3': ['3️⃣', '3⃣'],
                '4': ['4️⃣', '4⃣'], '5': ['5️⃣', '5⃣'], '6': ['6️⃣', '6⃣'],
                '7': ['7️⃣', '7⃣'], '8': ['8️⃣', '8⃣'], '9': ['9️⃣', '9⃣'],
                '10': ['0️⃣', '0⃣']
            }
            special_emojis = {'all': ['🔥'], 'yes': ['✅'], 'no': ['❌']}
            
            search_emojis = []
            if selected_num in number_emojis:
                search_emojis = number_emojis[selected_num]
            elif selected_num in special_emojis:
                search_emojis = special_emojis[selected_num]
            
            found_content = None
            for line in lines:
                line_stripped = line.strip()
                for emoji in search_emojis:
                    if line_stripped.startswith(emoji):
                        content = line_stripped[len(emoji):].strip()
                        if content.startswith('**'): content = content[2:]
                        if '**' in content: content = content.split('**')[0].strip()
                        if content.startswith(':') or content.startswith('-'): content = content[1:].strip()
                        # 파이프(|) 이후 내용 제거 (예: "전체 | ❌ 안올림" → "전체")
                        if '|' in content: content = content.split('|')[0].strip()
                        found_content = content[:100]
                        break
                if found_content: break
            
            if found_content:
                action_desc = f"\n📋 행위: {selection[1]} 옵션 - {found_content}"
            else:
                if selected_num == 'all': action_desc = "\n📋 행위: 🔥 모두 수행 (큐잉)"
                elif selected_num == 'yes': action_desc = "\n📋 행위: ✅ 승인"
                elif selected_num == 'no': action_desc = "\n📋 행위: ❌ 거절"
                else: action_desc = f"\n📋 행위: {selection[1]} 옵션 선택"
            
        except Exception as e:
            logger.warning(f"옵션 내용 추출 실패: {e}")
            action_desc = f"\n📋 행위: {selection[1]} 선택"
        
        # 메시지 전송
        forward_msg = f"<@{OPENCLAW_BOT_ID}> [선택] {user_name}님이 {selection[1]}을 선택했습니다.{action_desc}"
        await channel.send(forward_msg)
        
        logger.info(f"✅ 전달 완료: {forward_msg}")
        
    except Exception as e:
        logger.error(f"❌ 메시지 전송 실패: {e}")


@bot.command(name="ping")
async def ping(ctx):
    """봇 상태 확인"""
    await ctx.send("🏓 Pong! Noti-Bot 작동 중!")


def main():
    if not DISCORD_TOKEN:
        logger.error("❌ DISCORD_BOT_TOKEN이 설정되지 않음")
        return
    
    logger.info("🚀 Noti-Bot 시작...")
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
