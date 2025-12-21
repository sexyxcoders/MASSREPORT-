import os
import sys

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery
)

from info import Config, Txt


# ───────────────── START COMMAND ───────────────── #

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
        text=Txt.START_MSG.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# ───────────────── CALLBACK HANDLERS ───────────────── #

@Client.on_callback_query(filters.regex("^help$"))
async def help_callback(_, cq: CallbackQuery):
    await cq.message.edit_text(
        Txt.HELP_MSG,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅ Back", callback_data="back")]]
        )
    )


@Client.on_callback_query(filters.regex("^status$"))
async def status_callback(_, cq: CallbackQuery):
    await cq.message.edit_text(
        Txt.STATUS_MSG,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅ Back", callback_data="back")]]
        )
    )


@Client.on_callback_query(filters.regex("^about$"))
async def about_callback(_, cq: CallbackQuery):
    await cq.message.edit_text(
        Txt.ABOUT_MSG,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅ Back", callback_data="back")]]
        )
    )


@Client.on_callback_query(filters.regex("^back$"))
async def back_callback(bot: Client, cq: CallbackQuery):

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


# ───────────────── RESTART COMMAND ───────────────── #

@Client.on_message(
    filters.private
    & filters.command("restart")
    & filters.user(Config.SUDO)
)
async def restart_bot(_, message: Message):
    await message.reply_text("🔄 **Bot is restarting…**")
    os.execl(sys.executable, sys.executable, *sys.argv)