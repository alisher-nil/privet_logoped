"""
Модуль для хранения клавиатур
"""
from vkbottle import CtxStorage, Keyboard, KeyboardButtonColor, OpenLink, Text

from api_service import get_commands

ctx_storage = CtxStorage()

# Меню выбора роли
role_selection_keyboard = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Родитель"), color=KeyboardButtonColor.POSITIVE)
    .add(Text("Логопед"), color=KeyboardButtonColor.POSITIVE)
)


async def get_dynamic_keyboard(role: str):
    """Создание динамической клавиатуры в зависимости от роли пользователя"""
    keyboard = Keyboard(one_time=True, inline=False)
    commands = await get_commands()
    if commands:
        for command in commands:
            if command['role'] == role:
                ctx_storage.set(command['title'], command)
                keyboard.add(Text(command['title']),
                             color=KeyboardButtonColor.SECONDARY).row()
    if role == "parent":
        keyboard.add(Text("Задать вопрос логопеду"),
                     color=KeyboardButtonColor.SECONDARY).row()
    else:
        keyboard.add(Text("Задать вопрос руководителю"),
                     color=KeyboardButtonColor.SECONDARY).row()

    keyboard.add(Text("Сменить роль"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Обновить"), color=KeyboardButtonColor.NEGATIVE)
    return keyboard


async def get_links_attachments_keyboard(command_title: str, links: list,
                                         attachments: list):
    """Создание клавиатуры для ссылок и вложений"""
    keyboard = Keyboard(one_time=True, inline=False)
    for link in links:
        keyboard.add(OpenLink(link['url'], link['title'])).row()
    for attachment in attachments:
        keyboard.add(Text(attachment['title']),
                     color=KeyboardButtonColor.SECONDARY).row()
    keyboard.add(Text("Назад"), color=KeyboardButtonColor.NEGATIVE)
    return keyboard
