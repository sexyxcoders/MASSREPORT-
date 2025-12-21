import json
import subprocess
import sys
from pathlib import Path

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove
)

from info import Config, Txt

# ───────────────── CONSTANTS ───────────────── #

CONFIG_PATH = Path("config.json")


# ───────────────── HELPERS ───────────────── #

def load_config():
    if not CONFIG_PATH.exists():
        return None
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(data: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def session_exists(config: dict, session_str: str) -> bool:
    return any(acc["Session_String"] == session_str for acc in config.get("accounts", []))


def run_login(target: str, session_str: str):
    """
    Runs login.py to validate session and auto-join target.
    Expects JSON output with id & first_name.
    """
    process = subprocess.Popen(
        ["python", "login.py", target, session_str],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    code = process.wait()

    if code != 0:
        raise RuntimeError(stderr.decode("utf-8"))

    return json.loads(stdout.decode("utf-8"))


# ───────────────── ADD ACCOUNT ───────────────── #

@Client.on_message(
    filters.private
    & filters.user(Config.SUDO)
    & filters.command("add_account")
)
async def add_account(bot: Client, msg: Message):

    config = load_config()
    if not config:
        return await msg.reply_text(
            "❌ **Config not found**\n\nUse /make_config first.",
            reply_markup=ReplyKeyboardRemove()
        )

    # Ask for session string
    try:
        session_msg = await bot.ask(
            chat_id=msg.chat.id,
            text=Txt.SEND_SESSION_MSG,
            filters=filters.text,
            timeout=60,
            reply_markup=ReplyKeyboardRemove()
        )
    except:
        return await msg.reply_text("⏳ Timed out. Use /add_account again.")

    session_str = session_msg.text.strip()

    # Duplicate check
    if session_exists(config, session_str):
        return await msg.reply_text(
            "⚠️ **This account is already added.**",
            reply_markup=ReplyKeyboardRemove()
        )

    status = await msg.reply_text("⏳ **Validating account…**")

    # Validate session & auto-join target
    try:
        holder = run_login(config["Target"], session_str)
    except Exception as e:
        return await status.edit(
            f"❌ **Failed to add account**\n<code>{e}</code>"
        )

    # Append account
    new_account = {
        "Session_String": session_str,
        "OwnerUid": holder.get("id"),
        "OwnerName": holder.get("first_name", "Unknown")
    }

    config.setdefault("accounts", []).append(new_account)
    save_config(config)

    await status.edit(
        "✅ **Account added successfully**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("👥 View Accounts", callback_data="accounts")]]
        )
    )


# ───────────────── SHOW TARGET (COMMAND) ───────────────── #

@Client.on_message(
    filters.private
    & filters.user(Config.SUDO)
    & filters.command("target")
)
async def show_target(bot: Client, msg: Message):

    config = load_config()
    if not config or not config.get("Target"):
        return await msg.reply_text(
            "❌ **No target set**\nUse /set_target",
            reply_markup=ReplyKeyboardRemove()
        )

    try:
        chat = await bot.get_chat(config["Target"])
        text = (
            f"🎯 <b>Current Target</b>\n\n"
            f"• Name: <code>{chat.title}</code>\n"
            f"• Username: <code>@{chat.username}</code>\n"
            f"• ID: <code>{chat.id}</code>"
        )
    except:
        text = f"🎯 <b>Current Target</b>\n\n<code>{config['Target']}</code>"

    await msg.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔄 Change Target", callback_data="change_target")]]
        )
    )


# ───────────────── DELETE CONFIG (CONFIRM) ───────────────── #

@Client.on_message(
    filters.private
    & filters.user(Config.SUDO)
    & filters.command("del_config")
)
async def delete_config_prompt(_, msg: Message):

    buttons = [
        [InlineKeyboardButton("✅ Yes", callback_data="del_yes")],
        [InlineKeyboardButton("❌ No", callback_data="del_no")]
    ]

    await msg.reply_text(
        "⚠️ **Are you sure you want to delete the config?**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )