import os
import sys
import time
import psutil

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery
)

from info import Config, Txt


# ───────────────── START ───────────────── #

@Client.on_message(filters.private & filters.command("start"))
async def handle_start(bot: Client, message: Message):

    buttons = [
        [
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton("sᴛᴀᴛᴜs", callback_data="status")
        ],
        [
            InlineKeyboardButton("ɴᴇxᴀ//ɴᴇᴛᴡᴏʀᴋ", url="https://t.me/NexaCoders"),
            InlineKeyboardButton("ʙᴏᴛ ɪɴғᴏ", callback_data="about")
        ],
        [
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ", url="https://t.me/NexaMeetups")
        ]
    ]

    await message.reply_text(
        Txt.START_MSG.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# ───────────────── HELP ───────────────── #

@Client.on_callback_query(filters.regex("^help$"))
async def help_callback(_, cq: CallbackQuery):
    await cq.message.edit_text(
        Txt.HELP_MSG,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅ Back", callback_data="back")]]
        )
    )


# ───────────────── STATUS (FIXED) ───────────────── #

@Client.on_callback_query(filters.regex("^status$"))
async def status_callback(_, cq: CallbackQuery):

    uptime = time.strftime(
        "%Hh %Mm %Ss",
        time.gmtime(time.time() - Config.BOT_START_TIME)
    )

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    text = (
        "🟢 **Bot Status**\n\n"
        f"⏱ Uptime: `{uptime}`\n"
        f"🧠 CPU Usage: `{cpu}%`\n"
        f"💾 RAM Usage: `{ram}%`\n"
        f"📀 Disk Usage: `{disk}%`\n\n"
        "✅ Bot running normally"
    )

    await cq.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅ Back", callback_data="back")]]
        )
    )


# ───────────────── ABOUT (FIXED) ───────────────── #

@Client.on_callback_query(filters.regex("^about$"))
async def about_callback(bot: Client, cq: CallbackQuery):

    me = await bot.get_me()

    await cq.message.edit_text(
        Txt.ABOUT_MSG.format(me.username, me.first_name),
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅ Back", callback_data="back")]]
        )
    )


# ───────────────── BACK ───────────────── #

@Client.on_callback_query(filters.regex("^back$"))
async def back_callback(_, cq: CallbackQuery):

    buttons = [
        [
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help"),
            InlineKeyboardButton("sᴛᴀᴛᴜs", callback_data="status")
        ],
        [
            InlineKeyboardButton("ɴᴇxᴀ//ɴᴇᴛᴡᴏʀᴋ", url="https://t.me/NexaCoders"),
            InlineKeyboardButton("ʙᴏᴛ ɪɴғᴏ", callback_data="about")
        ],
        [
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ", url="https://t.me/NexaMeetups")
        ]
    ]

    await cq.message.edit_text(
        Txt.START_MSG.format(cq.from_user.mention),
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# ───────────────── RESTART ───────────────── #

@Client.on_message(
    filters.private
    & filters.command("restart")
    & filters.user(Config.SUDO)
)
async def restart_bot(_, message: Message):
    await message.reply_text("🔄 **Bot is restarting…**")
    os.execl(sys.executable, sys.executable, *sys.argv)