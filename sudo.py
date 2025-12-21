import os
import sys
from pyrogram import Client, filters
from pyrogram.types import Message

from info import Config


def restart_bot():
    os.execl(sys.executable, sys.executable, *sys.argv)


# ───────────────── ADD SUDO ───────────────── #

@Client.on_message(
    filters.private
    & filters.command("addsudo")
)
async def add_sudo(_, msg: Message):

    if msg.from_user.id != Config.OWNER:
        return await msg.reply_text("⛔ **Only OWNER can add sudo users**")

    if len(msg.command) != 2 or not msg.command[1].isdigit():
        return await msg.reply_text(
            "❌ **Usage:**\n`/addsudo <user_id>`"
        )

    new_uid = msg.command[1]

    current = os.environ.get("SUDO", "")
    sudo_list = set(current.split())

    if new_uid in sudo_list:
        return await msg.reply_text("⚠️ User is already SUDO")

    sudo_list.add(new_uid)
    os.environ["SUDO"] = " ".join(sudo_list)

    await msg.reply_text(
        f"✅ **User `{new_uid}` added as SUDO**\n\nRestarting bot…"
    )

    restart_bot()


# ───────────────── REMOVE SUDO ───────────────── #

@Client.on_message(
    filters.private
    & filters.command("delsudo")
)
async def del_sudo(_, msg: Message):

    if msg.from_user.id != Config.OWNER:
        return await msg.reply_text("⛔ **Only OWNER can remove sudo users**")

    if len(msg.command) != 2 or not msg.command[1].isdigit():
        return await msg.reply_text(
            "❌ **Usage:**\n`/delsudo <user_id>`"
        )

    uid = msg.command[1]
    sudo_list = set(os.environ.get("SUDO", "").split())

    if uid not in sudo_list:
        return await msg.reply_text("⚠️ User is not a SUDO")

    sudo_list.remove(uid)
    os.environ["SUDO"] = " ".join(sudo_list)

    await msg.reply_text(
        f"🗑 **User `{uid}` removed from SUDO**\n\nRestarting bot…"
    )

@Client.on_message(filters.private & filters.command("sudolist"))
async def sudo_list(_, msg):
    if msg.from_user.id != Config.OWNER:
        return await msg.reply_text("⛔ Owner only")

    sudo_users = os.environ.get("SUDO", "")
    await msg.reply_text(
        "👑 **SUDO USERS**\n\n" + "\n".join(sudo_users.split())
    )

    restart_bot()