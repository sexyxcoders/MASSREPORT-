import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

import psutil
from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup
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


def save_config(data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def humanbytes(size):
    if not size:
        return "0 B"
    power = 1024
    n = 0
    labels = ["B", "KB", "MB", "GB", "TB"]
    while size >= power and n < len(labels) - 1:
        size /= power
        n += 1
    return f"{round(size, 2)} {labels[n]}"


def clean_target(text: str):
    return re.sub(r"(https?://)|(t\.me/)|@", "", text).strip()


# ───────────────── CALLBACK HANDLER ───────────────── #

@Client.on_callback_query()
async def handle_query(bot: Client, query: CallbackQuery):
    data = query.data
    uid = query.from_user.id

    # ───── HELP ───── #
    if data == "help":
        buttons = [
            [
                InlineKeyboardButton("🎯 Target", callback_data="target"),
                InlineKeyboardButton("❌ Delete Config", callback_data="delete_conf")
            ],
            [
                InlineKeyboardButton("👥 Accounts", callback_data="accounts"),
                InlineKeyboardButton("⟸ Back", callback_data="home")
            ]
        ]
        return await query.message.edit(
            Txt.HELP_MSG,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # ───── SERVER STATUS ───── #
    if data == "server":
        uptime = time.strftime(
            "%Hh %Mm %Ss",
            time.gmtime(time.time() - Config.BOT_START_TIME)
        )

        total, used, free = shutil.disk_usage(".")
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent

        text = (
            "<b><u>Bot Status</u></b>\n\n"
            f"⏱ Uptime: <code>{uptime}</code>\n"
            f"🧠 CPU: <code>{cpu}%</code>\n"
            f"💾 RAM: <code>{ram}%</code>\n"
            f"📦 Disk: <code>{disk}%</code>\n"
            f"📂 Total: <code>{humanbytes(total)}</code>\n"
            f"📂 Used: <code>{humanbytes(used)}</code>\n"
            f"📂 Free: <code>{humanbytes(free)}</code>"
        )

        return await query.message.edit(
            text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⟸ Back", callback_data="home")]]
            )
        )

    # ───── ABOUT ───── #
    if data == "about":
        bot_info = await bot.get_me()
        return await query.message.edit(
            Txt.ABOUT_MSG.format(bot_info.username),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⟸ Back", callback_data="home")]]
            )
        )

    # ───── HOME ───── #
    if data == "home":
        buttons = [
            [
                InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help"),
                InlineKeyboardButton("sᴛᴀᴛᴜs", callback_data="server")
            ],
            [
                InlineKeyboardButton("ɴᴇxᴀ//ᴄᴏᴅᴇʀs", url="https://t.me/NexaCoders"),
                InlineKeyboardButton("ʙᴏᴛ ɪɴғᴏ", callback_data="about")
            ],
            [
                InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ", url="https://t.me/NexaMeetup")
            ]
        ]
        return await query.message.edit(
            Txt.START_MSG.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # ───── DELETE CONFIG ───── #
    if data == "delete_conf":
        if uid != Config.OWNER:
            return await query.answer("Owner only!", show_alert=True)

        buttons = [
            [InlineKeyboardButton("✅ Yes", callback_data="del_yes")],
            [InlineKeyboardButton("❌ No", callback_data="del_no")]
        ]
        return await query.message.edit(
            "⚠️ Are you sure you want to delete config?",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    if data == "del_yes":
        if CONFIG_PATH.exists():
            CONFIG_PATH.unlink()
        return await query.message.edit("✅ Config deleted")

    if data == "del_no":
        return await query.message.edit("❌ Operation cancelled")

    # ───── TARGET INFO ───── #
    if data == "target":
        config = load_config()
        if not config or not config.get("Target"):
            return await query.message.edit(
                "❌ No target set\nUse /set_target",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("⟸ Back", callback_data="help")]]
                )
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
            text = f"🎯 Target: <code>{config['Target']}</code>"

        return await query.message.edit(
            text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🔄 Change Target", callback_data="change_target")],
                    [InlineKeyboardButton("⟸ Back", callback_data="help")]
                ]
            )
        )

    # ───── CHANGE TARGET ───── #
    if data == "change_target":
        if uid != Config.OWNER:
            return await query.answer("Owner only!", show_alert=True)

        try:
            target_msg = await bot.ask(
                query.message.chat.id,
                Txt.SEND_TARGET_CHANNEL,
                filters=filters.text,
                timeout=60
            )
        except:
            return await query.message.edit("⏳ Timed out")

        new_target = clean_target(target_msg.text)
        config = load_config() or {}
        config["Target"] = new_target
        save_config(config)

        return await query.message.edit(
            f"✅ Target updated\n\n<code>{new_target}</code>"
        )

    # ───── ACCOUNTS LIST ───── #
    if data == "accounts":
        config = load_config()
        if not config or not config.get("accounts"):
            return await query.message.edit(
                "❌ No accounts added",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("⟸ Back", callback_data="help")]]
                )
            )

        buttons = [
            [InlineKeyboardButton(acc["OwnerName"], callback_data=f"acc_{acc['OwnerUid']}")]
            for acc in config["accounts"]
        ]
        buttons.append([InlineKeyboardButton("⟸ Back", callback_data="help")])

        return await query.message.edit(
            "👥 <b>Added Accounts</b>",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # ───── ACCOUNT INFO ───── #
    if data.startswith("acc_"):
        uid_clicked = int(data.split("_")[1])
        config = load_config()

        for acc in config.get("accounts", []):
            if acc["OwnerUid"] == uid_clicked:
                return await query.message.edit(
                    Txt.ACCOUNT_INFO.format(acc["OwnerName"], acc["OwnerUid"]),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("⟸ Back", callback_data="accounts")]]
                    )
                )

    # ───── FALLBACK ───── #
    await query.answer("Unknown action", show_alert=True)