import json
from pathlib import Path
from typing import Optional, Dict, List

# ───────────────── CONSTANT ───────────────── #

CONFIG_PATH = Path("config.json")


# ───────────────── CORE LOADERS ───────────────── #

def config_exists() -> bool:
    """Check if config.json exists"""
    return CONFIG_PATH.exists()


def load_config() -> Optional[Dict]:
    """Load full config.json"""
    if not CONFIG_PATH.exists():
        return None
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(data: Dict) -> None:
    """Save config.json safely"""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ───────────────── TARGET HELPERS ───────────────── #

def get_target() -> Optional[str]:
    """Return target (channel / group / user)"""
    config = load_config()
    if not config:
        return None
    return config.get("Target")


def set_target(new_target: str) -> bool:
    """Update target in config"""
    config = load_config()
    if not config:
        return False
    config["Target"] = new_target
    save_config(config)
    return True


# ───────────────── ACCOUNT HELPERS ───────────────── #

def get_accounts() -> List[Dict]:
    """Return all added Telegram accounts"""
    config = load_config()
    if not config:
        return []
    return config.get("accounts", [])


def get_account_count() -> int:
    """Return number of added accounts"""
    return len(get_accounts())


def get_max_accounts() -> int:
    """Return MaxAccounts limit"""
    config = load_config()
    if not config:
        return 0
    return int(config.get("MaxAccounts", 0))


def can_add_account() -> bool:
    """Check if new account can be added"""
    return get_account_count() < get_max_accounts()


def add_account(account_data: Dict) -> bool:
    """
    Add new account safely.
    account_data must contain:
    Session_String, OwnerUid, OwnerName
    """
    config = load_config()
    if not config:
        return False

    # Enforce limit
    if not can_add_account():
        return False

    # Prevent duplicates
    for acc in config.get("accounts", []):
        if acc["Session_String"] == account_data["Session_String"]:
            return False

    config.setdefault("accounts", []).append(account_data)
    save_config(config)
    return True


def remove_account(owner_uid: int) -> bool:
    """Remove account by Telegram user ID"""
    config = load_config()
    if not config:
        return False

    accounts = config.get("accounts", [])
    new_accounts = [a for a in accounts if a["OwnerUid"] != owner_uid]

    if len(accounts) == len(new_accounts):
        return False

    config["accounts"] = new_accounts
    save_config(config)
    return True


# ───────────────── MASS / REPORT HELPERS ───────────────── #

def get_runtime_summary() -> Dict:
    """Quick summary for status / report"""
    return {
        "config_exists": config_exists(),
        "target": get_target(),
        "accounts": get_account_count(),
        "max_accounts": get_max_accounts()
    }