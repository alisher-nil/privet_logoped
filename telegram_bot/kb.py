from aiogram.filters.callback_data import CallbackData
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from main_menu import chat_config
from schemas.menu import MenuItem

BUTTONS_PER_ROW = 2


class InlineButtonCallback(CallbackData, prefix="inline"):
    text: str
    callback: str


class MainMenuCallback(CallbackData, prefix="main_menu"):
    text: str = "main_menu"
    id: int


class AttachmentsCallback(CallbackData, prefix="attachments"):
    text: str = "attachments"
    path: str


def add_back_button(builder: InlineKeyboardBuilder):
    builder.row(
        InlineKeyboardButton(
            text="В главное меню",
            callback_data="backbutton_main",
        ),
        width=2,
    )


def main_kb(user_role: str):
    builder = InlineKeyboardBuilder()
    for menu_item in chat_config.main_menu_items.values():
        if menu_item.role == user_role:
            builder.button(
                text=menu_item.title,
                callback_data=MainMenuCallback(id=menu_item.id),
            )
    builder.adjust(BUTTONS_PER_ROW)
    builder.row(
        InlineKeyboardButton(
            text="❓ Задать вопрос", callback_data="ask_a_question"
        ),
        width=2,
    )
    builder.row(
        InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings"),
        width=2,
    )
    return builder.as_markup()


def menu_item_kb(menu_item: MenuItem):
    builder = InlineKeyboardBuilder()
    for link in menu_item.links:
        builder.button(
            text=link.title,
            url=link.url,
        )

    for attachment in menu_item.attachments:
        builder.button(
            text=attachment.title,
            callback_data=AttachmentsCallback(path=attachment.file),
        )
    builder.adjust(BUTTONS_PER_ROW)
    add_back_button(builder)
    return builder.as_markup()


def registration_kb(items: dict[str, str]):
    builder = InlineKeyboardBuilder()
    for button, callback in items.items():
        builder.button(
            text=button,
            callback_data=InlineButtonCallback(text=button, callback=callback),
        )
    return builder.as_markup()


def settings_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="✍🏻 Сменить роль", callback_data="change_role")
    add_back_button(builder)
    return builder.as_markup()


def change_role_kb(role_dict: dict[str, str]):
    builder = InlineKeyboardBuilder()
    for button, callback in role_dict.items():
        builder.button(
            text=button,
            callback_data=InlineButtonCallback(text=button, callback=callback),
        )
    add_back_button(builder)
    return builder.as_markup()


def ask_a_question_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="✍🏻 Написать вопрос", callback_data="make_question")
    add_back_button(builder)
    return builder.as_markup()


def after_question_kb():
    builder = InlineKeyboardBuilder()
    add_back_button(builder)
    return builder.as_markup()
