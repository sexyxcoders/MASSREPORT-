import json
import re
from pathlib import Path

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove
)

from info import Config, Txt

# ───────────────── CONSTANT ───────────────── #

CONFIG_PATH = Path("config.json")


# ───────────────── HELPERS ───────────────── #

def clean_target(text: str) -> str:
    return re.sub(r"(https?://)|(t\.me/)|@", "", text).strip()


# ───────────────── MAKE CONFIG ───────────────── #

@Client.on_message(
    filters.private
    & filters.user(Config.SUDO)
    & filters.command("make_config")
)
async def make_config(bot: Client, msg: Message):

    if CONFIG_PATH.exists():
        return await msg.reply_text(
            "⚠️ **Config already exists**\n\nUse /del_config to remove it first.",
            reply_markup=ReplyKeyboardRemove()
        )

    # Ask number of accounts (reference only)
    try:
        count_msg = await bot.ask(
            msg.chat.id,
            Txt.SEND_NUMBERS_MSG,
            filters=filters.text,
            timeout=60,
            reply_markup=ReplyKeyboardRemove()
        )
    except:
        return await msg.reply_text("⏳ Timed out. Use /make_config again.")

    if not count_msg.text.isnumeric():
        return await msg.reply_text("❌ **Please send a valid number.**")

    max_accounts = int(count_msg.text)

    # Ask target
    try:
        target_msg = await bot.ask(
            msg.chat.id,
            Txt.SEND_TARGET_CHANNEL,
            filters=filters.text,
            timeout=60
        )
    except:
        return await msg.reply_text("⏳ Timed out. Use /make_config again.")

    target = clean_target(target_msg.text)

    try:
        await bot.get_chat(target)
    except Exception as e:
        return await msg.reply_text(
            f"❌ **Invalid target**\n<code>{e}</code>"
        )

    # Create config WITHOUT sessions
    config = {
        "Target": target,
        "MaxAccounts": max_accounts,
        "accounts": []
    }

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

    await msg.reply_text(
        "✅ **Config created successfully**\n\n"
        f"🎯 Target: <code>{target}</code>\n"
        f"👥 Account limit: <code>{max_accounts}</code>\n\n"
        "Now add accounts using:\n"
        "`/add_account`",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("➕ Add Account", callback_data="accounts")]]
        )
    )


# ───────────────── SEE ACCOUNTS ───────────────── #

@Client.on_message(
    filters.private
    & filters.user(Config.SUDO)
    & filters.command("see_accounts")
)
async def see_accounts(_, msg: Message):

    if not CONFIG_PATH.exists():
        return await msg.reply_text(
            "❌ **No config found**\nUse /make_config first."
        )

    config = json.load(open(CONFIG_PATH, "r", encoding="utf-8"))
    total = len(config.get("accounts", []))

    await msg.reply_text(
        Txt.ADDED_ACCOUNT.format(total),
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("👥 View Accounts", callback_data="accounts")]]
        )
    )