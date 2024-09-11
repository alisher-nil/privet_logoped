from http import HTTPStatus

from aiogram.fsm.context import FSMContext

from api_service import (
    get_user_by_id,
    post_new_user,
    post_user_question,
    put_user_by_id,
)


async def get_user_data(user_id: int, state: FSMContext):
    data, status = await get_user_by_id(user_id)
    if status != HTTPStatus.OK:
        return None
    return data


async def check_user_register(user_id: int) -> tuple[bool, int]:
    data, status = await get_user_by_id(user_id)
    if status == HTTPStatus.OK:
        return True, status, data
    return False, status, None


async def user_registration(user_id: int, user_role: str) -> tuple[bool, int]:
    data, status = await post_new_user(
        telegram_id=user_id, user_role=user_role
    )
    if status == HTTPStatus.CREATED:
        return True, status
    return False, status


async def user_update(user_id: int, user_role: str) -> tuple[bool, int]:
    data, status = await put_user_by_id(
        telegram_id=user_id, user_role=user_role
    )
    if status == HTTPStatus.OK:
        return True, status
    return False, status


async def post_question(
    user_id: int, text: str, message_id: int
) -> tuple[bool, int]:
    data, status = await post_user_question(
        telegram_id=user_id, question_text=text, message_id=message_id
    )
    if status == HTTPStatus.CREATED:
        return True, status
    return False, status
