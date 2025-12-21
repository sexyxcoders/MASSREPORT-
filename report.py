import sys
import json
import asyncio
from pathlib import Path

from pyrogram import Client
from pyrogram.raw.functions.account import ReportPeer
from pyrogram.raw.types import *

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"

# ───────────────── CONSTANTS ───────────────── #

CONFIG_PATH = Path("config.json")

# ───────────────── REPORT REASONS ───────────────── #

REASON_MAP = {
    "Report for child abuse": InputReportReasonChildAbuse,
    "Report for copyrighted content": InputReportReasonCopyright,
    "Report for impersonation": InputReportReasonFake,
    "Report an irrelevant geogroup": InputReportReasonGeoIrrelevant,
    "Report an illegal durg": InputReportReasonIllegalDrugs,
    "Reason for Pornography": InputReportReasonPornography,
    "Report for spam": InputReportReasonSpam,
    "Report for offensive person detail": InputReportReasonPersonalDetails,
    "Report for Violence": InputReportReasonViolence
}


def get_reason(reason_text: str):
    cls = REASON_MAP.get(reason_text)
    if not cls:
        raise ValueError("Invalid report reason")
    return cls()


# ───────────────── CORE LOGIC ───────────────── #

async def report_with_account(target: str, session: str, name: str, reason, message: str):
    async with Client(
        name=f"report_{name}",
        session_string=session,
        no_updates=True
    ) as app:

        peer = await app.resolve_peer(target)

        # Channel / Group
        if hasattr(peer, "channel_id"):
            input_peer = InputPeerChannel(
                channel_id=peer.channel_id,
                access_hash=peer.access_hash
            )

        # User
        elif hasattr(peer, "user_id"):
            input_peer = InputPeerUser(
                user_id=peer.user_id,
                access_hash=peer.access_hash
            )

        else:
            raise RuntimeError("Unsupported peer type")

        report = ReportPeer(
            peer=input_peer,
            reason=reason,
            message=message
        )

        return await app.invoke(report)


async def main(report_message: str):

    if not CONFIG_PATH.exists():
        raise RuntimeError("config.json not found")

    config = json.load(open(CONFIG_PATH, "r", encoding="utf-8"))

    target = config.get("Target")
    accounts = config.get("accounts", [])

    if not target or not accounts:
        raise RuntimeError("Target or accounts missing")

    # Reason is embedded in report_message header (already chosen in bot)
    reason = get_reason(report_message)

    for acc in accounts:
        try:
            result = await report_with_account(
                target=target,
                session=acc["Session_String"],
                name=acc["OwnerName"],
                reason=reason,
                message=report_message
            )
            print(f"✅ Reported by {acc['OwnerName']}")

        except Exception as e:
            print(f"❌ Failed from {acc['OwnerName']} → {e}")


# ───────────────── ENTRY POINT ───────────────── #

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python report.py <report_message>")
        sys.exit(1)

    asyncio.run(main(sys.argv[1]))