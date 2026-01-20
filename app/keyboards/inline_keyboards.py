from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from callbacks import DeleteProductCallbackFactory, EditProductCallbackFactory


def get_edit_product_keyboard(
        product_id: int,
        i18n: dict[str, Any]
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=i18n['btn_edit_product'],
                callback_data=EditProductCallbackFactory(product_id=product_id).pack()
            ),
            InlineKeyboardButton(
                text=i18n['btn_delete_product'],
                callback_data=DeleteProductCallbackFactory(product_id=product_id).pack()
            ),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
