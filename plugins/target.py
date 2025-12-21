import json
from pathlib import Path
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardRemove

from info import Config, Txt

# ---------------- CONFIG ---------------- #

CONFIG_PATH = Path("config.json")

DEFAULT_CONFIG = {
    "Target": None
}

# ---------------- HELPERS ---------------- #

def load_config():
    if not CONFIG_PATH.exists():
        return DEFAULT_CONFIG.copy()

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(data: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ---------------- COMMAND HANDLERS ---------------- #

@Client.on_message(
    filters.private
    & filters.user(Config.OWNER)
    & filters.command("make_config")
)
async def make_config(_, msg: Message):
    """
    Create or reset config.json
    """
    save_config(DEFAULT_CONFIG.copy())

    await msg.reply_text(
        "✅ **Config created successfully**\n\n"
        "Now set a target using:\n"
        "`/set_target @channel | -100xxxx | user_id`",
        reply_markup=ReplyKeyboardRemove()
    )


@Client.on_message(
    filters.private
    & filters.user(Config.OWNER)
    & filters.command("del_config")
)
async def del_config(_, msg: Message):
    """
    Delete config.json
    """
    if CONFIG_PATH.exists():
        CONFIG_PATH.unlink()
        await msg.reply_text(
            "🗑 **Config deleted successfully**",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await msg.reply_text(
            "❌ **No config found**",
            reply_markup=ReplyKeyboardRemove()
        )


@Client.on_message(
    filters.private
    & filters.user(Config.OWNER)
    & filters.command("set_target")
)
async def set_target(_, msg: Message):
    """
    Set target channel/group/user
    """
    if len(msg.command) < 2:
        return await msg.reply_text(
            "❌ **Usage:**\n"
            "`/set_target @channel | -100xxxx | user_id`",
            reply_markup=ReplyKeyboardRemove()
        )

    target = msg.text.split(None, 1)[1].strip()

    config = load_config()
    config["Target"] = target
    save_config(config)

    await msg.reply_text(
        f"🎯 **Target set successfully**\n\n"
        f"Target: `{target}`",
        reply_markup=ReplyKeyboardRemove()
    )


@Client.on_message(
    filters.private
    & filters.user(Config.OWNER)
    & filters.command("target")
)
async def show_target(_, msg: Message):
    """
    Show current target
    """
    if not CONFIG_PATH.exists():
        return await msg.reply_text(
            "❌ **No config found**\nUse /make_config first",
            reply_markup=ReplyKeyboardRemove()
        )

    config = load_config()
    target = config.get("Target")

    if not target:
        return await msg.reply_text(
            "⚠️ **Target not set**\n\nUse:\n"
            "`/set_target @channel | -100xxxx | user_id`",
            reply_markup=ReplyKeyboardRemove()
        )

    await msg.reply_text(
        f"🎯 **Current Target**\n\n"
        f"`{target}`",
        reply_markup=ReplyKeyboardRemove()
    )
