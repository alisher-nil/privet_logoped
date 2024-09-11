"""
Модуль для обработки команд
"""
from pathlib import Path

from vkbottle import CtxStorage, Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message
from vkbottle.http import aiohttp

import text as txt
from config import MEDIA_ROOT
from api_service import (
    check_user_exists,
    create_or_update_user,
    send_question_to_api,
)
from keyboards import (
    get_dynamic_keyboard,
    get_links_attachments_keyboard,
    role_selection_keyboard,
)

ctx_storage = CtxStorage()


async def main_menu(message: Message):
    """Главное меню для пользователя"""
    user_id = message.from_id
    user_exists, user_data = await check_user_exists(user_id)

    if user_exists:
        role = user_data.get("role", "parent")
        role_text = txt.ROLE_PARENT if role == "parent" else txt.ROLE_LOGOPED
        dynamic_keyboard = await get_dynamic_keyboard(role)
        await message.answer(
            txt.WELCOME_BACK.format(role_text=role_text),
            keyboard=dynamic_keyboard
        )
    else:
        await message.answer(
            txt.WELCOME_NEW_USER,
            keyboard=role_selection_keyboard
        )


async def select_role(message: Message):
    """Выбор роли пользователем"""
    role = message.text.lower()
    if role not in [txt.PARENT_ROLE, txt.LOGOPED_ROLE]:
        await message.answer(txt.SELECT_ROLE_ERROR)
        return
    role_en = "parent" if role == txt.PARENT_ROLE else "logoped"
    user_id = message.from_id
    user_exists, _ = await check_user_exists(user_id)
    success = await create_or_update_user(user_id, role_en, user_exists)
    if success:
        dynamic_keyboard = await get_dynamic_keyboard(role_en)
        await message.answer(
            txt.ROLE_REGISTERED.format(role=role.capitalize()),
            keyboard=dynamic_keyboard
        )
        await message.answer(txt.MAIN_MENU, keyboard=dynamic_keyboard)
    else:
        await message.answer(txt.ROLE_REGISTER_ERROR)


async def change_role(message: Message):
    """Изменение роли пользователя"""
    await message.answer(txt.CHANGE_ROLE_PROMPT,
                         keyboard=role_selection_keyboard)


class AskQuestionState:
    """Состояния для вопросов"""
    ASKING_LOGOPED = "asking_logoped"
    ASKING_DIRECTOR = "asking_director"


async def ask_logoped_question(message: Message):
    """Начало диалога с логопедом"""
    ctx_storage.set(message.peer_id, AskQuestionState.ASKING_LOGOPED)
    await message.answer(
        txt.ASK_QUESTION_PROMPT,
        keyboard=Keyboard().add(Text(txt.CANCEL),
                                color=KeyboardButtonColor.NEGATIVE)
    )


async def ask_director_question(message: Message):
    """Начало диалога с директором"""
    ctx_storage.set(message.peer_id, AskQuestionState.ASKING_DIRECTOR)
    await message.answer(
        txt.ASK_QUESTION_PROMPT,
        keyboard=Keyboard().add(Text(txt.CANCEL),
                                color=KeyboardButtonColor.NEGATIVE)
    )


async def handle_question_response(message: Message):
    """Обработка ответа на вопрос"""
    state = ctx_storage.get(message.peer_id)
    if state in [AskQuestionState.ASKING_LOGOPED,
                 AskQuestionState.ASKING_DIRECTOR]:
        if message.text == txt.CANCEL:
            ctx_storage.delete(message.peer_id)
            await return_to_role_menu(message)
        else:
            role = (txt.TO_LOGOPED if state == AskQuestionState.ASKING_LOGOPED
                    else txt.TO_DIRECTOR)
            await send_question(message, message.text, role)
            ctx_storage.delete(message.peer_id)
    else:
        command = (ctx_storage.get(message.text) or
                   ctx_storage.get(message.peer_id))
        if command:
            description = command.get('description', '')
            title = command.get('title', txt.NO_DESCRIPTION)
            message_text = description if description else title
            links = command.get('links', [])
            attachments = command.get('attachments', [])
            if message.text in [att['title'] for att in attachments]:
                await send_attachment(message, message.text)
            elif links or attachments:
                links_keyboard = await get_links_attachments_keyboard(
                    command['title'], links, attachments)
                await message.answer(message_text, keyboard=links_keyboard)
                ctx_storage.set(message.peer_id, command)
            else:
                await message.answer(message_text)
                await return_to_role_menu(message)
        else:
            await message.answer(txt.COMMAND_NOT_FOUND)
            await return_to_role_menu(message)
    if not (links or attachments):
        ctx_storage.delete(message.peer_id)


async def send_attachment(message: Message, file_title: str):
    """Отправка вложения пользователю"""
    command = ctx_storage.get(message.peer_id)
    if command:
        attachment = next((att for att in command['attachments'] if
                           att['title'] == file_title), None)
        if attachment:
            file_path = Path(MEDIA_ROOT) / attachment['file']
            if not file_path.exists():
                await message.answer(txt.FILE_NOT_FOUND)
                return
            async with aiohttp.ClientSession() as session:
                upload_server = await message.ctx_api.docs.get_messages_upload_server(
                    peer_id=message.peer_id)
                with open(file_path, 'rb') as file:
                    async with session.post(
                            upload_server.upload_url,
                            data={'file': file}) as upload_response:
                        upload_data = await upload_response.json()
                saved_file = await message.ctx_api.docs.save(
                    file=upload_data['file'], title=file_path.name)
                file_id = f"doc{saved_file.doc.owner_id}_{saved_file.doc.id}"
                await message.answer(attachment=file_id)
            links = command.get('links', [])
            attachments = command.get('attachments', [])
            if links or attachments:
                links_keyboard = await get_links_attachments_keyboard(
                    command['title'], links, attachments)
                await message.answer(txt.SELECT_NEXT_ACTION,
                                     keyboard=links_keyboard)
        else:
            await message.answer(txt.ATTACHMENT_NOT_FOUND)
    else:
        await message.answer(txt.COMMAND_NOT_FOUND)


async def send_question(message: Message, question_text: str, role: str):
    """Отправка вопроса"""
    user_id = message.from_id
    success = await send_question_to_api(user_id, question_text, message.id)
    if success:
        await message.answer(txt.QUESTION_SENT.format(role=role))
    else:
        await message.answer(txt.QUESTION_SEND_ERROR)
    await return_to_role_menu(message)
    ctx_storage.delete(message.peer_id)


async def return_to_role_menu(message: Message):
    """Возвращение пользователя в меню в зависимости от роли"""
    user_id = message.from_id
    user_exists, user_data = await check_user_exists(user_id)
    if user_exists:
        role = user_data.get("role", "parent")
        dynamic_keyboard = await get_dynamic_keyboard(role)
        role_text = txt.ROLE_PARENT if role == "parent" else txt.ROLE_LOGOPED
        await message.answer(txt.RETURNING_TO_MENU.format(role_text=role_text),
                             keyboard=dynamic_keyboard)
    else:
        await message.answer(txt.RETURN_TO_MENU_ERROR,
                             keyboard=role_selection_keyboard)
    ctx_storage.delete(message.peer_id)


async def refresh_commands_menu(message: Message):
    """Обновление меню команд"""
    user_id = message.from_id
    user_exists, user_data = await check_user_exists(user_id)
    if user_exists:
        role = user_data.get("role", "parent")
        role_text = txt.ROLE_PARENT if role == "parent" else txt.ROLE_LOGOPED
        dynamic_keyboard = await get_dynamic_keyboard(role)
        await message.answer(txt.MENU_UPDATED.format(role_text=role_text),
                             keyboard=dynamic_keyboard)
    else:
        await message.answer(txt.RETURN_TO_MENU_ERROR,
                             keyboard=role_selection_keyboard)
