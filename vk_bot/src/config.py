"""
Модуль для настройки бота
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

VK_BOT_TOKEN = os.getenv('VK_BOT_TOKEN')
BACKEND_URL = os.getenv('BACKEND_URL')

BASE_DIR = Path(__file__).parent.parent.parent
MEDIA_ROOT = Path.joinpath(
    BASE_DIR, Path(os.getenv("MEDIA_ROOT", "/media"))
)

VK_USERS_URL = f"{BACKEND_URL}/api/v1/vk/users/"
VK_USER_QUERY_URL = f"{BACKEND_URL}/api/v1/vk/user_query/"
VK_ANSWERS_URL = f"{BACKEND_URL}/api/v1/vk/answers/"
VK_CONFIRM_ANSWERS_URL = f"{BACKEND_URL}/api/v1/vk/answers/confirm_sent/"
VK_COMMANDS_URL = f"{BACKEND_URL}/api/v1/common/commands/"
RESPONSE_CHECK_INTERVAL = 60
