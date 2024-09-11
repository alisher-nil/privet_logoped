"""
Модуль для взаимодействия с API
"""
from typing import Any, Dict, List, Optional, Tuple
from http import HTTPStatus

import requests

from config import (
    VK_USERS_URL,
    VK_USER_QUERY_URL,
    VK_ANSWERS_URL,
    VK_CONFIRM_ANSWERS_URL,
    VK_COMMANDS_URL,
)


async def check_user_exists(
        user_id: int
) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """Проверка существования пользователя"""
    response = requests.get(f"{VK_USERS_URL}{user_id}")
    return response.status_code == HTTPStatus.OK, (
        response.json() if response.status_code == HTTPStatus.OK else None
    )


async def create_or_update_user(
        user_id: int, role: str, user_exists: bool
) -> bool:
    """Создание или обновление данных пользователя"""
    data = {"user_id": user_id, "role": role}
    if user_exists:
        response = requests.patch(f"{VK_USERS_URL}{user_id}/", json=data)
    else:
        response = requests.post(VK_USERS_URL, json=data)
    return response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]


async def send_question_to_api(
        user_id: int, question_text: str, message_id: int
) -> bool:
    """Отправка вопроса"""
    data = {
        "user_id": user_id,
        "question_text": question_text,
        "message_id": message_id,
    }
    response = requests.post(VK_USER_QUERY_URL, json=data)
    return response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]


async def get_answers() -> Optional[List[Dict[str, Any]]]:
    """Получение списка ответов"""
    response = requests.get(VK_ANSWERS_URL)
    return response.json() if response.status_code == HTTPStatus.OK else None


async def confirm_answers(ids: List[int]) -> None:
    """Подтверждение получения ответов"""
    requests.post(VK_CONFIRM_ANSWERS_URL, json={"ids": ids})


async def get_commands() -> Optional[List[Dict[str, Any]]]:
    """Получение списка команд для динамической клавиатуры"""
    response = requests.get(VK_COMMANDS_URL)
    return response.json() if response.status_code == HTTPStatus.OK else None
