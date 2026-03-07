from collections.abc import Sequence
from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks import (
    AddProductToCartCallback,
    CartManagingCallback,
    DeleteProductCallbackFactory,
    EditProductCallbackFactory,
    CategoryCallbackFactory,
    PageCallbackFactory,
    PaginationCallbackFactory
)

from database.models import Category, InfoPage, Product


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


def get_pages_buttons(
        i18n: dict[str, Any],
        category_id: int,
        prev_page: int | None = None,
        next_page: int | None = None
) -> list[InlineKeyboardButton]:
    """List of buttons for pagination."""

    pages_btn = list()

    if prev_page:
        pages_btn.append(InlineKeyboardButton(
            text=i18n['btn_previous'],
            callback_data=PaginationCallbackFactory(
                page=prev_page,
                category_id=category_id
            ).pack()
        ))
    if next_page:
        pages_btn.append(InlineKeyboardButton(
            text=i18n['btn_next'],
            callback_data=PaginationCallbackFactory(
                page=next_page,
                category_id=category_id
            ).pack()
        ))

    return pages_btn


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

    categories_buttons = [
        InlineKeyboardButton(
            text=i18n[cat.name],
            callback_data=CategoryCallbackFactory(category_id=cat.id).pack()
        )
        for cat in categories
    ]
    buttons = {
        i18n['btn_back']: PageCallbackFactory(name='main').pack(),
        i18n['cart_name']: PageCallbackFactory(name='cart').pack(),
    }

    builder = InlineKeyboardBuilder()
    builder.attach(
        InlineKeyboardBuilder.from_markup(inline_keyboard_factory(
            buttons=buttons,
            sizes=(2, 2))
        )
    )
    builder.row(*categories_buttons, width=2)

    return builder.as_markup()


def product_list_keyboard(
        i18n: dict[str, Any],
        category_id: int,
        product: Product,
        user_id: int,
        prev_page: int | None = None,
        next_page: int | None = None
) -> InlineKeyboardMarkup:
    """Product list keyboard."""

    first_row_buttons = [
        InlineKeyboardButton(
            text=i18n['btn_back'],
            callback_data=PageCallbackFactory(name='catalog').pack()
        ),
        InlineKeyboardButton(
            text=i18n['cart_name'],
            callback_data=PageCallbackFactory(name='cart').pack()
        ),
    ]

    buy_btn = InlineKeyboardButton(
        text=i18n['btn_buy'],
        callback_data=AddProductToCartCallback(
            product_id=product.id,
            user_id=user_id
        ).pack()
    )

    pagination_buttons = get_pages_buttons(
        i18n,
        category_id=category_id,
        prev_page=prev_page,
        next_page=next_page
    )

    builder = InlineKeyboardBuilder()
    builder.row(*first_row_buttons[:2], width=2)
    builder.row(buy_btn)
    builder.row(*pagination_buttons, width=2)

    return builder.as_markup()


def empty_cart_keyboard(
        i18n: dict[str, Any],
):
    """Keyboard for empty cart page."""

    buttons = {
        i18n['btn_back']: PageCallbackFactory(name='catalog').pack(),
        i18n['btn_to_main']: PageCallbackFactory(name='main').pack(),
    }
    return inline_keyboard_factory(buttons=buttons, sizes=(2,))


def cart_list_keyboard(
        i18n: dict[str, Any],
        category_id: int,
        product: Product,
        user_id: int,
        prev_page: int | None = None,
        next_page: int | None = None
):
    """Cart list keyboard."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=i18n['btn_delete_product'],
            callback_data=CartManagingCallback(
                action='delete',
                user_id=user_id,
                product_id=product.id
            ).pack()
        ),
        InlineKeyboardButton(
            text=i18n['decrease'],
            callback_data=CartManagingCallback(
                action='decrease',
                user_id=user_id,
                product_id=product.id
            ).pack()
        ),
        InlineKeyboardButton(
            text=i18n['increase'],
            callback_data=CartManagingCallback(
                action='increase',
                user_id=user_id,
                product_id=product.id
            ).pack()
        ),
        width=3
    )
    builder.row(
        *get_pages_buttons(
            i18n,
            category_id=category_id,
            prev_page=prev_page,
            next_page=next_page
        ),
        width=2
    )
    builder.row(
        InlineKeyboardButton(
            text=i18n['btn_to_main'],
            callback_data=PageCallbackFactory(name='main').pack()
        ),
        InlineKeyboardButton(
            text=i18n['btn_order'],
            callback_data='order'
        ),
        width=2
    )

    return builder.as_markup()
