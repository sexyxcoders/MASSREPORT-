import os
import time

class Config(object):
    # Pyrogram Client
    API_ID    = int(os.environ.get("API_ID", "29896633"))
    API_HASH  = os.environ.get("API_HASH", "7a8a6dd1c08f6ffc33645885bb3ecf77")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8474871278:AAF4XBwAwIaIPrD3he4r_lWT5dCCD1jWUaQ")

    # Other Configs
    BOT_START_TIME = time.time()
    OWNER = int(os.environ.get("OWNER", "5867783630"))
    SUDO = list(map(int, os.environ.get("SUDO", "8067478942").split()))

    # Web Response Config
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "8080"))


class Txt(object):

    SEND_NUMBERS_MSG = "SEND THE TOTAL NUMBER YOU HAVE"

    ASK_NUMBERS_MSG = "How many numbers do you have?"

    SEND_TARGET_CHANNEL = """
SEND THE TARGET CHANNEL LINK or USERNAME

For e.g :- @username or https://t.me/example
"""

    SEND_SESSION_MSG = """
SEND SESSION STRING

Generate a Session String from @
"""

    SEND_API_ID = """
SEND API ID

Api_id can be obtained from my.telegram.org
"""

    SEND_API_HASH = """
SEND API HASH

Api_hash can be obtained from my.telegram.org
"""

    MAKE_CONFIG_DONE_MSG = """
Your {} accounts have been added 👥

And logged into the target channel/group to report it. ✅

Click the button below to see the number of Telegram accounts you added.
"""

    ADDED_ACCOUNT = """
You have added {} accounts 👥

Click the button below to see more information about the Telegram accounts you added.
"""

    ACCOUNT_INFO = """
<b>Name :-</b> <code>{0}</code>
<b>User Id :-</b> <code>{1}</code>
"""

    REPORT_CHOICE = """
SELECT REASON FOR REPORT 👤

1. Report for child abuse
2. Report for copyrighted content
3. Report for impersonation
4. Report an irrelevant geo-group
5. Report for illegal drugs
6. Report for violence
7. Report for offensive personal details
8. Report for pornography
9. Report for spam

Select 1–9:
"""

    SEND_NO_OF_REPORT_MSG = """
SELECT NUMBER OF REPORTS 👤

Send number of reports you want to send to @{}.

Bot will keep reporting until it reaches the target number. 🎯
"""

    START_MSG = """
Hi {},

This bot reports channels or groups in mass using Telegram account session strings generated via @.

This bot is created by @itzdaxx
"""

    HELP_MSG = """
🔆 HELP

📚 Available commands:
⏣ /start - Check I'm alive 
⏣ /make_config - Make config 
⏣ /del_config - Delete config
⏣ /target - See target channel
⏣ /see_accounts - See all added accounts
⏣ /add_account - Add new account
⏣ /report - Report target
⏣ /restart - Restart bot

💢 Features:
► Report a single channel/group with multiple IDs
► Choose report type
► Change target channel/group anytime
► Add unlimited accounts
► Accounts will auto-join the target
► Only session string needed
► Server CPU/RAM monitor
"""

    ABOUT_MSG = """
- My Name : <a href="https://t.me/{}">{}</a>
- Creator : <a href="https://t.me/itzdaxx">@itzdaxx</a>
- Library : Pyrogram
- Language : Python 3
- Database : MongoDB
- Bot Server : Anywhere
"""