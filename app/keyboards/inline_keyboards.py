from collections.abc import Sequence
from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks import (
    DeleteProductCallbackFactory,
    EditProductCallbackFactory,
    CategoryCallbackFactory,
    PageCallbackFactory
)

from database.models import Product, Category, InfoPage


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
        buttons[i18n[f'{page.name}_name']] = PageCallbackFactory(name=page.name).pack()

    return inline_keyboard_factory(buttons=buttons, sizes=(3,))


def main_menu_keyboard(i18n: dict[str, Any]) -> InlineKeyboardMarkup:
    """Main page keyboard."""

    buttons = {
        i18n['catalog_name']: PageCallbackFactory(name='catalog').pack(),
        i18n['cart_name']: PageCallbackFactory(name='cart').pack(),
        i18n['about_name']: PageCallbackFactory(name='about').pack(),
        i18n['payment_name']: PageCallbackFactory(name='payment').pack(),
        i18n['shipping_name']: PageCallbackFactory(name='shipping').pack()
    }

    return inline_keyboard_factory(buttons=buttons, sizes=(2, 2, 1))


def catalog_page_keyboard(
        i18n: dict[str, Any],
        categories: Sequence[Category]
) -> InlineKeyboardMarkup:
    """Categories page keyboard."""

    categories_buttons = {
        i18n[cat.name]: CategoryCallbackFactory(category_id=cat.id).pack()
        for cat in categories
    }
    buttons = {
        i18n['btn_back']: PageCallbackFactory(name='main').pack(),
        i18n['cart_name']: PageCallbackFactory(name='cart').pack(),
    }
    buttons.update(categories_buttons)

    return inline_keyboard_factory(buttons=buttons, sizes=(2, 2))
