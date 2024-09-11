from http import HTTPStatus
from pathlib import Path

from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile

from config import AVAILABLE_USER_ROLES, MEDIA_ROOT
from exceptions import handle_api_error
from kb import (
    AttachmentsCallback,
    InlineButtonCallback,
    MainMenuCallback,
    ask_a_question_kb,
    after_question_kb,
    change_role_kb,
    main_kb,
    menu_item_kb,
    registration_kb,
    settings_kb,
)
from main_menu import chat_config
from text import TEXT_FOR_MAIN_KB
from utils import (
    check_user_register,
    post_question,
    user_registration,
    user_update,
)


router = Router()


class RegisterForm(StatesGroup):
    role = State()


class UserMenu(StatesGroup):
    main = State()
    asking_question = State()


@router.message(CommandStart())
async def start_handler(msg: Message, state: FSMContext):
    registered, status, user_data = await check_user_register(
        user_id=msg.from_user.id
    )

    if registered:
        await state.set_state(UserMenu.main)
        await state.update_data(user_role=user_data["role"])
        await msg.answer(
            text=f"Приветствую, {msg.from_user.username}\n{TEXT_FOR_MAIN_KB}",
            reply_markup=main_kb(user_role=user_data["role"]),
        )
    else:
        if status == HTTPStatus.NOT_FOUND:
            await msg.answer(
                text=(
                    f"Добро пожаловать, {msg.from_user.username}!\n"
                    f"Пожалуйста, пройдите регистрацию:"
                ),
            )
            await msg.answer(
                text="<b>ВЫБЕРИТЕ РОЛЬ</b>",
                reply_markup=registration_kb(items=AVAILABLE_USER_ROLES),
            )
            await state.set_state(RegisterForm.role)
        else:
            await handle_api_error(obj=msg, status=status)


@router.callback_query(MainMenuCallback.filter(F.text == "main_menu"))
async def my_callback_foo(
    callback: types.CallbackQuery,
    callback_data: MainMenuCallback,
    state: FSMContext,
):
    menu_item = chat_config.main_menu_items.get(callback_data.id)
    if menu_item is None:
        await callback.answer("Меню устарело, перенаправляю в главное меню")
        user_data = await state.get_data()
        await callback.answer(
            text=TEXT_FOR_MAIN_KB,
            reply_markup=main_kb(user_role=user_data["role"]),
        )
        return
    await callback.answer()
    await callback.message.edit_text(
        text=menu_item.description,
        reply_markup=menu_item_kb(menu_item),
    )


@router.callback_query(AttachmentsCallback.filter(F.text == "attachments"),
                       flags={'probably_old': True})
async def attachments_handler(
    callback: types.CallbackQuery, callback_data: AttachmentsCallback
):
    file_path = Path.joinpath(MEDIA_ROOT, callback_data.path)
    if not Path.exists(file_path):
        await callback.answer(text="Не удалось найти файл.")
        return
    file = FSInputFile(file_path)
    await callback.answer()
    print("sending now")
    await callback.message.answer_document(document=file)


@router.callback_query(
    RegisterForm.role,
    InlineButtonCallback.filter(F.callback.in_(AVAILABLE_USER_ROLES.values())),
)
async def role_chosen(
    callback: types.CallbackQuery,
    callback_data: InlineButtonCallback,
    state: FSMContext,
):
    await state.update_data(chosen_role=callback_data.callback)
    created, status = await user_registration(
        user_id=callback.from_user.id, user_role=callback_data.callback
    )
    if created:
        await callback.message.edit_text(
            text=(
                f"Ваша роль <b>{callback_data.text}</b> зарегистрирована,"
                "вы можете её сменить в настройках."
            )
        )
        await state.clear()
        await callback.message.answer(
            text=("Нажмите /start\n" "Чтобы открыть меню")
        )
    else:
        await handle_api_error(obj=callback, status=status)


@router.callback_query(
    RegisterForm.role,
)
async def role_chosen_incorrectly(
    callback: types.CallbackQuery, callback_data: InlineButtonCallback
):
    await callback.message.answer(
        text=(
            "‼️Неизвестная роль, выбирайте из списка‼️\n"
            "<b>ВЫБЕРИТЕ РОЛЬ</b>"
        ),
        reply_markup=registration_kb(items=AVAILABLE_USER_ROLES),
    )


@router.callback_query(F.data == "settings", flags={'probably_old': True})
async def settings_menu(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await callback.message.edit_text(
        text=(f'<b>Ваши настройки</b>\n' f'Роль: {user_data["user_role"]}'),
        reply_markup=settings_kb(),
    )


@router.callback_query(F.data == "change_role", flags={'probably_old': True})
async def change_role_menu(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    text = f'Текущая роль: {user_data["user_role"]}'
    if callback.message.text != text:
        await callback.message.edit_text(
            text=text,
            reply_markup=change_role_kb(role_dict=AVAILABLE_USER_ROLES),
        )


@router.callback_query(
    UserMenu.main,
    InlineButtonCallback.filter(F.callback.in_(AVAILABLE_USER_ROLES.values())),
)
async def role_changed(
    callback: types.CallbackQuery,
    callback_data: InlineButtonCallback,
    state: FSMContext,
):
    await state.update_data(user_role=callback_data.callback)
    created, status = await user_update(
        user_id=callback.from_user.id, user_role=callback_data.callback
    )
    if created:
        await change_role_menu(callback, state)
    else:
        await handle_api_error(obj=callback, status=status)


@router.callback_query(F.data == "ask_a_question",
                       flags={'probably_old': True})
async def ask_a_question_menu(
    callback: types.CallbackQuery,
):
    await callback.message.edit_text(
        text=(
            "Нажмите кнопку <b>написать вопрос</b>, "
            "а затем напишете свой вопрос. Ваше обращение будет "
            "зарегистрированно, а ответ придёт в чате с этим ботом."
        ),
        reply_markup=ask_a_question_kb(),
    )
    await callback.answer()


@router.callback_query(F.data == "make_question")
async def making_a_question_message(
    callback: types.CallbackQuery, state: FSMContext
):
    await state.set_state(UserMenu.asking_question)
    await callback.message.edit_text(
        text=("⬇️⬇️<b>НАПИШИТЕ ВОПРОС</b>⬇️⬇️ "),
    )
    await callback.answer()


@router.message(
    UserMenu.asking_question,
    flags={'probably_old': True}
)
async def asking_question(message: Message, state: FSMContext):
    created, status = await post_question(
        user_id=message.from_user.id,
        text=message.text,
        message_id=message.message_id,
    )
    if created:
        await message.answer(
            text=(f"<b>Ваше сообщение:</b> {message.text}\n"
                  "<b>Зарегистрировано.</b>"),
            reply_markup=after_question_kb()
        )
    else:
        await handle_api_error(obj=message, status=status)
    await state.set_state(UserMenu.main)


@router.callback_query(F.data.startswith("backbutton_"),
                       flags={'probably_old': True})
async def back_to_previous_menu(
    callback: types.CallbackQuery, state: FSMContext
):
    action = callback.data.split("_")[1]
    user_data = await state.get_data()

    if action == "main":
        await callback.message.edit_text(
            text=TEXT_FOR_MAIN_KB,
            reply_markup=main_kb(user_role=user_data["user_role"]),
        )
        await callback.answer()

    if action == "settings":
        await settings_menu(callback, state)
