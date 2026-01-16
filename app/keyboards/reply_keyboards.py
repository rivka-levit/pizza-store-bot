from typing import Any
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_start_kb(i18n: dict[str, str | Any]) -> ReplyKeyboardMarkup:
    """Starting keyboard"""

    buttons = [
            KeyboardButton(text=i18n['btn_menu']),
            KeyboardButton(text=i18n['btn_about']),
            KeyboardButton(text=i18n['btn_payment']),
            KeyboardButton(text=i18n['btn_shipping'])
        ]

    builder = ReplyKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(2, 2)

    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder=i18n['input_field_placeholder'],
        one_time_keyboard=True
    )


def reply_kb_factory(
        *buttons: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int, ...] = (2,)
) -> ReplyKeyboardMarkup:
    """Create and return reply keyboard with custom buttons."""

    builder = ReplyKeyboardBuilder()

    for index, text in enumerate(buttons, 1):
        btn = KeyboardButton(text=text)
        if request_contact and request_contact == index:
            btn.request_contact = True
        elif request_location and request_location == index:
            btn.request_location = True
        builder.add(btn)

    builder.adjust(*sizes)

    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder=placeholder,
    )


def get_admin_keyboard(i18n: dict[str, str | Any]) -> ReplyKeyboardMarkup:
    buttons = [
        i18n['btn_add_item'],
        i18n['btn_edit_item'],
        i18n['btn_del_item'],
        i18n['btn_just_looking'],
    ]
    return reply_kb_factory(
        *buttons,
        placeholder=i18n['placeholder_admin_kb'],
        sizes=(2, 1, 1)
    )