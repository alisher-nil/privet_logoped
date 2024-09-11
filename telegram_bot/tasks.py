from http import HTTPStatus

from aiogram import Bot

from api_service import get_answers, post_confirm_sent, request_main_menu
from main_menu import chat_config
from schemas.menu import CommandList


async def send_answers_to_users(bot: Bot):
    answers, status = await get_answers()

    if status == HTTPStatus.OK:
        sent_ids = []
        for answer in answers:
            await bot.send_message(
                answer["user_query"]["user_id"],
                text=answer["answer_text"],
                reply_to_message_id=answer["user_query"]["message_id"],
            )
            sent_ids.append(answer["id"])
        if sent_ids:
            await post_confirm_sent(sent_ids=sent_ids)


async def refresh_main_menu():
    data = await request_main_menu()
    menu = CommandList.model_validate(data)
    chat_config.main_menu_items = {item.id: item for item in menu.root}
