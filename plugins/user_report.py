import json
import os
import subprocess
import sys
from pathlib import Path

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)

from info import Config, Txt

# ---------------- CONFIG ---------------- #

CONFIG_PATH = Path("config.json")
REPORT_FILE = "report.txt"

# ---------------- CORE EXECUTOR ---------------- #

async def run_report_process(report_message: str):
    """
    Executes report.py with the given report message
    """
    process = subprocess.Popen(
        ["python", "report.py", report_message],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = process.communicate()
    return_code = process.wait()

    if return_code == 0:
        return stdout.decode("utf-8"), True
    else:
        return stderr.decode("utf-8"), False


# ---------------- MAIN REPORT FLOW ---------------- #

async def CHOICE_OPTION(bot: Client, msg: Message, choice_number: int):

    # Check config
    if not CONFIG_PATH.exists():
        return await msg.reply_text(
            "**No config found!**\n\nUse /make_config first.",
            reply_markup=ReplyKeyboardRemove()
        )

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Prevent parallel runs
    if Path(REPORT_FILE).exists():
        return await msg.reply_text(
            "⏳ **A report process is already running. Please wait.**",
            reply_markup=ReplyKeyboardRemove()
        )

    # Ask for report text
    try:
        report_msg = await bot.ask(
            chat_id=msg.chat.id,
            text="✍️ **Send the report message you want to use**",
            filters=filters.text,
            timeout=60,
            reply_markup=ReplyKeyboardRemove()
        )
    except:
        return await bot.send_message(
            msg.chat.id,
            "❌ Timed out.\nUse /report again."
        )

    # Ask for number of reports
    try:
        count_msg = await bot.ask(
            chat_id=msg.chat.id,
            text=Txt.SEND_NO_OF_REPORT_MSG.format(config["Target"]),
            filters=filters.text,
            timeout=30
        )
    except:
        return await bot.send_message(
            msg.chat.id,
            "❌ Timed out.\nUse /report again."
        )

    if not count_msg.text.isnumeric():
        return await msg.reply_text(
            "❌ **Please send a valid number.**\nUse /report again."
        )

    total = int(count_msg.text)
    sent = 0

    status = await bot.send_message(
        msg.chat.id,
        "⏳ **Please wait… Processing reports**"
    )

    # Execute reports
    try:
        while sent < total:
            output, ok = await run_report_process(report_msg.text)

            if not ok:
                await bot.send_message(
                    msg.chat.id,
                    f"❌ Error occurred:\n<code>{output}</code>"
                )
                break

            with open(REPORT_FILE, "a+", encoding="utf-8") as f:
                f.write(output + "\n")

            sent += 1

    except Exception as e:
        print(
            f"Error on line {sys.exc_info()[-1].tb_lineno}:",
            type(e).__name__,
            e
        )
        return await msg.reply_text(f"❌ **Error:** `{e}`")

    await status.delete()

    # Final message
    await msg.reply_text(
        f"✅ **Report sent successfully**\n\n"
        f"🎯 Target: @{config['Target']}\n"
        f"📊 Total reports: {sent}",
        reply_markup=ReplyKeyboardRemove()
    )

    # Append summary
    with open(REPORT_FILE, "a+", encoding="utf-8") as f:
        f.write(
            f"\n\nTarget @{config['Target']} reported {sent} times ✅"
        )

    # Send TXT report
    await bot.send_document(
        chat_id=msg.chat.id,
        document=REPORT_FILE
    )

    os.remove(REPORT_FILE)


# ---------------- COMMAND HANDLERS ---------------- #

@Client.on_message(
    filters.private
    & filters.user(Config.OWNER)
    & filters.command("report")
)
async def handle_report(bot: Client, cmd: Message):

    keyboard = [
        ["1", "2"],
        ["3", "4"],
        ["5", "6"],
        ["7", "8"],
        ["9"]
    ]

    await bot.send_message(
        chat_id=cmd.from_user.id,
        text=Txt.REPORT_CHOICE,
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


# ---------------- NUMBER SELECTION ---------------- #

@Client.on_message(filters.regex("^1$"))
async def one(bot, msg): await CHOICE_OPTION(bot, msg, 1)

@Client.on_message(filters.regex("^2$"))
async def two(bot, msg): await CHOICE_OPTION(bot, msg, 2)

@Client.on_message(filters.regex("^3$"))
async def three(bot, msg): await CHOICE_OPTION(bot, msg, 3)

@Client.on_message(filters.regex("^4$"))
async def four(bot, msg): await CHOICE_OPTION(bot, msg, 4)

@Client.on_message(filters.regex("^5$"))
async def five(bot, msg): await CHOICE_OPTION(bot, msg, 5)

@Client.on_message(filters.regex("^6$"))
async def six(bot, msg): await CHOICE_OPTION(bot, msg, 6)

@Client.on_message(filters.regex("^7$"))
async def seven(bot, msg): await CHOICE_OPTION(bot, msg, 7)

@Client.on_message(filters.regex("^8$"))
async def eight(bot, msg): await CHOICE_OPTION(bot, msg, 8)

@Client.on_message(filters.regex("^9$"))
async def nine(bot, msg): await CHOICE_OPTION(bot, msg, 9)