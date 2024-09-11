"""
Модуль для запуска бота
"""
from vkbottle.bot import Bot

from config import VK_BOT_TOKEN
from handlers import (
    ask_director_question,
    ask_logoped_question,
    change_role,
    handle_question_response,
    main_menu,
    refresh_commands_menu,
    return_to_role_menu,
    select_role,
)
from tasks import polling_task

bot = Bot(token=VK_BOT_TOKEN)

# Регистрация обработчиков
bot.on.message(text=["Начать", "Меню"])(main_menu)
bot.on.message(text=["Родитель", "Логопед"])(select_role)
bot.on.message(text="Сменить роль")(change_role)
bot.on.message(text="Задать вопрос логопеду")(ask_logoped_question)
bot.on.message(text="Задать вопрос руководителю")(ask_director_question)
bot.on.message(text="Назад")(return_to_role_menu)
bot.on.message(text="Обновить")(refresh_commands_menu)
bot.on.message()(handle_question_response)

bot.loop_wrapper.add_task(polling_task(bot))
bot.run_forever()
