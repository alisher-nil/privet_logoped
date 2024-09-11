from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.dispatcher.flags import get_flag

from utils import (
    check_user_register,
)
from text import TEXT_FOR_CLIENT_ERROR


class CheckOldMenuMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        probably_old = get_flag(data, "probably_old")
        if probably_old:
            registered, status, user_data = await check_user_register(
                user_id=data['event_from_user'].id
            )
            if registered:
                state = data["state"]
                role = await state.get_data()
                role = role.get('role')
                if role is None:
                    await state.update_data(user_role=user_data["role"])
            else:
                await event.answer()
                await event.message.edit_text(
                    text=TEXT_FOR_CLIENT_ERROR
                )
                return
        return await handler(event, data)
