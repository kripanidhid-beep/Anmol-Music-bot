import asyncio
import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
from yt_dlp import YoutubeDL

from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING

# BOT + USER CLIENT
bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

user = Client(
    session_name=SESSION_STRING,
    api_id=API_ID,
    api_hash=API_HASH
)

call = PyTgCalls(user)

ydl_opts = {
    "format": "bestaudio",
    "quiet": True,
    "outtmpl": "downloads/%(id)s.%(ext)s"
}

if not os.path.exists("downloads"):
    os.mkdir("downloads")


@bot.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply_text("🎵 Music Bot Alive!\n/play <song name>")


@bot.on_message(filters.command("play") & filters.group)
async def play(_, msg):
    if len(msg.command) < 2:
        return await msg.reply("❌ Song name do")

    query = " ".join(msg.command[1:])
    await msg.reply("🔎 Searching...")

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
        file = f"downloads/{info['id']}.{info['ext']}"

    await call.join_group_call(
        msg.chat.id,
        AudioPiped(file, HighQualityAudio()),
    )

    await msg.reply(f"▶️ Playing: **{info['title']}**")


async def main():
    await bot.start()
    await user.start()
    await call.start()
    print("🎵 Music Bot Started")
    await asyncio.Event().wait()


asyncio.run(main())
