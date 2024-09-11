from typing import Union

from aiogram.types import Message, CallbackQuery

from text import (
    TEXT_FOR_CLIENT_ERROR,
    TEXT_FOR_SERVER_ERROR,
)


async def handle_api_error(obj: Union[Message, CallbackQuery], status: int):
    if isinstance(obj, CallbackQuery):
        if 400 <= status < 500:
            await obj.message.edit_text(
                text=TEXT_FOR_CLIENT_ERROR,
            )
        else:
            await obj.message.edit_text(
                text=TEXT_FOR_SERVER_ERROR,
            )
    else:
        if 400 <= status < 500:
            await obj.answer(
                text=TEXT_FOR_CLIENT_ERROR,
            )
        else:
            await obj.answer(
                text=TEXT_FOR_SERVER_ERROR,
            )
