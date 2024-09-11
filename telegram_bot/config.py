import logging
import os
from pathlib import Path
from urllib.parse import urljoin

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_TIMEZONE = os.getenv("BOT_TIMEZONE", "Europe/Moscow")

MAIN_SERVER_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/")
COMMANDS_URL = urljoin(MAIN_SERVER_URL, "api/v1/common/commands/")
TELEGRAM_ROOT_URL = urljoin(MAIN_SERVER_URL, "api/v1/telegram/")
USER_URL = urljoin(TELEGRAM_ROOT_URL, "users/")
QUESTION_URL = urljoin(TELEGRAM_ROOT_URL, "user_query/")
ANSWERS_URL = urljoin(TELEGRAM_ROOT_URL, "answers/")
ANSWERS_CONFIRM_URL = urljoin(ANSWERS_URL, "confirm_sent/")

BASE_DIR = Path(__file__).parent.parent
MEDIA_ROOT = Path.joinpath(BASE_DIR, Path(os.getenv("MEDIA_ROOT", "/media")))

AVAILABLE_USER_ROLES = {
    "Родитель": "parent",
    "Логопед": "logoped",
}
