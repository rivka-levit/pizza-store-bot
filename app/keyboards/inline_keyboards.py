from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from sqlalchemy.ext.asyncio import AsyncSession

from callbacks import DeleteProductCallbackFactory, EditProductCallbackFactory, CategoryCallbackFactory

from database.models import Product, Category
from database.orm_query import orm_get_categories


def inline_keyboard_factory(
        *,
        buttons: dict[str, str],
        sizes: tuple[int, ...] = (2,)
) -> InlineKeyboardMarkup:
    """Base function to create any inline keyboard."""

    builder = InlineKeyboardBuilder()

    for text, data in buttons.items():
        builder.add(InlineKeyboardButton(text=text, callback_data=data))

    return builder.adjust(*sizes).as_markup()



def get_edit_product_keyboard(
        product: Product,
        i18n: dict[str, Any]
) -> InlineKeyboardMarkup:
    """Keyboard to edit or delete a product."""

    buttons = {
        f'{i18n['btn_edit_product']}': f'{EditProductCallbackFactory(
                                                product_id=product.id, 
                                                product_name=product.name
                                            ).pack()}',
        f'{i18n['btn_delete_product']}': f'{DeleteProductCallbackFactory(
                                                product_id=product.id, 
                                                product_name=product.name
                                            ).pack()}'
    }
    return inline_keyboard_factory(buttons=buttons)


def get_categories_keyboard(
        categories: list[Category],
        i18n: dict[str, Any]
) -> InlineKeyboardMarkup:
    """Keyboard to choose the category."""

    buttons = {
        i18n[category.name]: CategoryCallbackFactory(category_id=category.id).pack()
        for category in categories
    }
    return inline_keyboard_factory(buttons=buttons)
