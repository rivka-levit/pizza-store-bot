from collections.abc import Sequence
from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from sqlalchemy.ext.asyncio import AsyncSession

from callbacks import (
    DeleteProductCallbackFactory,
    EditProductCallbackFactory,
    CategoryCallbackFactory,
    PageCallbackFactory
)

from database.models import Product, Category, InfoPage
from database.orm_query import orm_get_info_page


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
        categories: Sequence[Category],
        i18n: dict[str, Any]
) -> InlineKeyboardMarkup:
    """Keyboard to choose the category."""

    buttons = {
        i18n[category.name]: CategoryCallbackFactory(category_id=category.id).pack()
        for category in categories
    }
    return inline_keyboard_factory(buttons=buttons)


def page_choice_keyboard(
        pages: Sequence[InfoPage],
        i18n: dict[str, Any]
) -> InlineKeyboardMarkup:
    """Keyboard to choose a page."""

    buttons = dict()

    for page in pages:
        buttons[i18n[f'{page.name}_name']] = PageCallbackFactory(
            id=page.id,
            name=page.name
        ).pack()

    return inline_keyboard_factory(buttons=buttons, sizes=(3,))


def main_menu_keyboard(
        i18n: dict[str, Any],
        pages: Sequence[InfoPage]
) -> InlineKeyboardMarkup:
    """Main page keyboard."""

    page_data: dict[str, int] = dict()
    for page in pages:
        page_data[page.name] = page.id

    buttons = {
        i18n['catalog_name'] : PageCallbackFactory(
            id=page_data['catalog'],
            name='catalog'
        ).pack(),
        i18n['cart_name']: PageCallbackFactory(
            id=page_data['cart'],
            name='cart'
        ).pack(),
        i18n['about_name']: PageCallbackFactory(
            id=page_data['about'],
            name='about'
        ).pack(),
        i18n['payment_name']: PageCallbackFactory(
            id=page_data['payment'],
            name='payment'
        ).pack(),
        i18n['shipping_name']: PageCallbackFactory(
            id=page_data['shipping'],
            name='shipping'
        ).pack()
    }

    return inline_keyboard_factory(buttons=buttons, sizes=(2, 2, 1))
