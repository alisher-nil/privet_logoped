import aiohttp
from http import HTTPStatus
from urllib.parse import urljoin

from config import (
    ANSWERS_CONFIRM_URL,
    ANSWERS_URL,
    COMMANDS_URL,
    QUESTION_URL,
    USER_URL,
)


async def post_new_user(telegram_id: int, user_role: str) -> tuple[dict, int]:
    data = {
        "user_id": telegram_id,
        "role": user_role,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=USER_URL, json=data) as response:
            data = await response.json()
            return data, response.status


async def put_user_by_id(telegram_id: int, user_role: str) -> tuple[dict, int]:
    url = urljoin(USER_URL, f"{telegram_id}/")
    data = {
        "user_id": telegram_id,
        "role": user_role,
    }
    async with aiohttp.ClientSession() as session:
        async with session.put(url=url, json=data) as response:
            data = await response.json()
            return data, response.status


async def get_user_by_id(telegram_id: int) -> tuple[dict, int]:
    url = urljoin(USER_URL, f"{telegram_id}/")
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            data = await response.json()
            return data, response.status


async def post_user_question(
    telegram_id: int, question_text: str, message_id: int
) -> tuple[dict, int]:
    data = {
        "user_id": telegram_id,
        "question_text": question_text,
        "message_id": message_id,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=QUESTION_URL, json=data) as response:
            data = await response.json()
            return data, response.status


async def get_answers() -> tuple[dict, int]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=ANSWERS_URL) as response:
            data = await response.json()
            return data, response.status


async def post_confirm_sent(sent_ids: list[int]) -> tuple[dict, int]:
    data = {"ids": sent_ids}
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=ANSWERS_CONFIRM_URL, json=data
        ) as response:
            data = await response.json()
            return data, response.status


async def request_main_menu() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=COMMANDS_URL) as response:
            if response.status != HTTPStatus.OK:
                return []
            return await response.json()
