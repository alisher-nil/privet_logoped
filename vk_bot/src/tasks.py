"""
Модуль для выполнения фоновых задач
"""
import asyncio

from vkbottle import Bot

import text as txt
from api_service import confirm_answers, get_answers
from config import RESPONSE_CHECK_INTERVAL
# from vk_bot.src.keyboards import get_dynamic_keyboard


# async def update_dynamic_commands():
#    """Обновление динамических команд для родителя и логопеда"""
#     await get_dynamic_keyboard("parent")
#     await get_dynamic_keyboard("logoped")


async def check_for_answers(bot: Bot):
    """Проверка наличия новых ответов и отправка их пользователям"""
    answers = await get_answers()
    if answers:
        sent_ids = []
        for answer in answers:
            try:
                user_id = answer["user_query"]["user_id"]
                question_text = answer["user_query"]["question_text"]
                answer_text = answer["answer_text"]
                message_text = txt.ANSWER_TEMPLATE.format(
                    question_text=question_text, answer_text=answer_text)
                await bot.api.messages.send(user_id=user_id,
                                            message=message_text, random_id=0)
                sent_ids.append(answer["id"])
            except Exception as e:
                print(
                    f"Не удалось отправить ответ пользователю {user_id}: {e}")
        if sent_ids:
            await confirm_answers(sent_ids)


async def polling_task(bot: Bot):
    """Задача для постоянной проверки наличия ответов"""
    while True:
        await check_for_answers(bot)
#         await update_dynamic_commands()
        await asyncio.sleep(RESPONSE_CHECK_INTERVAL)
