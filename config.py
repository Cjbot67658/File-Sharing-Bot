# config.py (robust version)
import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()

def getenv_str(name: str, default: str = None, required: bool = False) -> str:
    v = os.environ.get(name, default)
    if required and (v is None or v == ""):
        raise Exception(f"Environment variable {name} is required but not set.")
    return v

def getenv_int(name: str, default: int = None, required: bool = False) -> int:
    v = os.environ.get(name, None)
    if v is None or v == "":
        if required and default is None:
            raise Exception(f"Environment variable {name} is required but not set.")
        return default
    try:
        return int(v)
    except ValueError:
        raise Exception(f"Environment variable {name} must be an integer. Got: {v!r}")

# Required values
TG_BOT_TOKEN = getenv_str("TG_BOT_TOKEN", required=True)       # Bot token from @BotFather
APP_ID = getenv_int("APP_ID", required=True)                   # my.telegram.org
API_HASH = getenv_str("API_HASH", required=True)               # my.telegram.org

# Channel id (required if your bot uses a DB channel)
CHANNEL_ID = getenv_int("CHANNEL_ID", None, required=False)    # -100xxxxxxxxxx OR None

# OWNER ID (required)
OWNER_ID = getenv_int("OWNER_ID", required=True)

# Optional / defaults
PORT = getenv_str("PORT", "8080")
DB_URI = getenv_str("DATABASE_URL", "")
DB_NAME = getenv_str("DATABASE_NAME", "filesharexbot")

FORCE_SUB_CHANNEL = getenv_int("FORCE_SUB_CHANNEL", 0)
JOIN_REQUEST_ENABLE = getenv_str("JOIN_REQUEST_ENABLED", None)

TG_BOT_WORKERS = getenv_int("TG_BOT_WORKERS", 4)

START_PIC = getenv_str("START_PIC", "")
START_MSG = getenv_str("START_MESSAGE", "Hello {first}\n\nI can store private files in Specified Channel and other users can access it from special link.")
FORCE_MSG = getenv_str("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>")
CUSTOM_CAPTION = getenv_str("CUSTOM_CAPTION", None)

PROTECT_CONTENT = True if getenv_str('PROTECT_CONTENT', "False") == "True" else False

AUTO_DELETE_TIME = getenv_int("AUTO_DELETE_TIME", 0)
AUTO_DELETE_MSG = getenv_str("AUTO_DELETE_MSG", "This file will be automatically deleted in {time} seconds. Please ensure you have saved any necessary content before this time.")
AUTO_DEL_SUCCESS_MSG = getenv_str("AUTO_DEL_SUCCESS_MSG", "Your file has been successfully deleted. Thank you for using our service. ✅")

DISABLE_CHANNEL_BUTTON = getenv_str("DISABLE_CHANNEL_BUTTON", "False") == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot!"

# ADMINS
ADMINS = []
admins_raw = getenv_str("ADMINS", "")
if admins_raw:
    for x in admins_raw.split():
        try:
            ADMINS.append(int(x))
        except ValueError:
            raise Exception(f"Invalid ADMIN id: {x!r} in ADMINS env variable.")

# Ensure owner in admins
if OWNER_ID not in ADMINS:
    ADMINS.append(OWNER_ID)

# Optional extra admin (if you want to keep a backup id)
try:
    EXTRA_ADMIN = 1250450587
    if EXTRA_ADMIN not in ADMINS:
        ADMINS.append(EXTRA_ADMIN)
except Exception:
    pass

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
