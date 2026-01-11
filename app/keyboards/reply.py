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
