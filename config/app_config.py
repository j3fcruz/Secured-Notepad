# config/app_config.py
# ---------------------------------------------------------
# 🔐 Secure Notepad Pro - Config (Environment-based)
# ---------------------------------------------------------

import os
import sys
from dotenv import load_dotenv

# ---------------------------------------------------------
# 🌍 Load .env File (Development Mode)
# ---------------------------------------------------------
ENV_FILE = ".env"
if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)
else:
    print(f"⚠️ Warning: {ENV_FILE} not found. Using default values.")

# ---------------------------------------------------------
# 📦 Resource Path (Supports PyInstaller)
# ---------------------------------------------------------
def resource_path(relative_path: str) -> str:
    """
    Resolve absolute path to a resource.
    Works both in development and PyInstaller compiled builds.
    Automatically falls back to ./assets if missing.
    """
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        path = os.path.join(base_path, relative_path)
        if os.path.exists(path):
            return path

        # Fallback to local assets folder
        fallback = os.path.join(os.getcwd(), "assets", os.path.basename(relative_path))
        return fallback if os.path.exists(fallback) else relative_path
    except Exception:
        return relative_path

# ---------------------------------------------------------
# 🧱 Application Metadata
# ---------------------------------------------------------
APP_NAME = os.getenv("APP_NAME", "Secure Notepad Pro")
HASH_NAME = os.getenv("HASH_NAME", "securenotepadpro")
APP_VERSION = os.getenv("APP_VERSION", "2.0.0")
AUTHOR = os.getenv("AUTHOR", "Marco Polo")
APP_DEVELOPER = os.getenv("APP_DEVELOPER", "PatronHubDevs")
COPYRIGHT_YEAR = os.getenv("COPYRIGHT_YEAR", "2025")
COPYRIGHT = f"© {COPYRIGHT_YEAR} {APP_NAME}. All rights reserved."
ABOUT_APP = os.getenv("ABOUT_APP", "Military-grade encryption meets modern note-taking.")

DESCRIPTION = os.getenv(
    "DESCRIPTION",
    f"""{APP_NAME} by {AUTHOR} is an enterprise-grade encrypted text editor 
built for professionals, developers, and privacy advocates. It combines elegant 
UI design with advanced cryptographic protection to keep your notes safe and secure."""
)

# ---------------------------------------------------------
# 🖼️ Resource & Asset Paths
# ---------------------------------------------------------
ICON_PATH = resource_path(os.getenv("ICON_PATH", "assets/icons/lock_icon.png"))
ABOUT_ICON_PATH = resource_path(os.getenv("ABOUT_ICON_PATH", "assets/icons/about_icon.png"))
DONATE_ICON_PATH = resource_path(os.getenv("DONATE_ICON_PATH", "assets/icons/donate_icon.png"))
HELP_ICON_PATH = resource_path(os.getenv("HELP_ICON_PATH", "assets/icons/help_icon.png"))
MAYA_QR_PATH = resource_path(os.getenv("MAYA_QR_PATH", "assets/resources/maya_qr.bin"))
MAYA_QR_KEY = os.getenv("MAYA_QR_KEY", "").encode()

# ---------------------------------------------------------
# 🌐 External Links (Public-Safe)
# ---------------------------------------------------------
GITHUB_ID = os.getenv("GITHUB_ID", "https://github.com/j3fcruz/Secured-Notepad")
KOFI_ID = os.getenv("KOFI_ID", "https://ko-fi.com/marcopolo55681")
PAYPAL_ID = os.getenv("PAYPAL_ID", "https://paypal.me/jofreydelacruz13")

BTC_NAME = os.getenv("BTC_NAME", "Bitcoin (BTC) Address")
BTC_ID = os.getenv("BTC_ID", "1BcWJT8gBdZSPwS8UY39X9u4Afu1nZSzqk")

ETH_NAME = os.getenv("ETH_NAME", "Ethereum (ETH) Address")
ETH_ID = os.getenv("ETH_ID", "0xcd5eef32ff4854e4cefa13cb308b727433505bf4")

# ---------------------------------------------------------
# ⚙️ Environment Detection
# ---------------------------------------------------------
APP_ENV = os.getenv("APP_ENV", "development").lower()
IS_PRODUCTION = APP_ENV == "production"
IS_DEVELOPMENT = APP_ENV == "development"

def safe_log(msg: str):
    """Safe logging (avoids PyCharm/IDE crash issues)."""
    try:
        print(msg)
    except Exception:
        pass

safe_log(f"✅ Secure Notepad Pro config loaded successfully ({APP_ENV.upper()} MODE)")
