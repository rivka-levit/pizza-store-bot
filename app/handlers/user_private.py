from typing import Any

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, or_f
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from sqlalchemy.ext.asyncio import AsyncSession

from callbacks import (
    AddProductToCartCallback,
    CategoryCallbackFactory,
    PageCallbackFactory,
    PaginationCallbackFactory
)

from database.orm_query import (
    orm_add_to_cart,
    orm_get_categories,
    orm_get_info_page,
    orm_get_products
)

from filters.chat_types import ChatTypeFilter
from filters.reply_buttons import ReplyButtonsFilter

from keyboards.inline_keyboards import (
    catalog_page_keyboard,
    main_menu_keyboard,
    product_list_keyboard
)

from utils.pagination import Paginator

router = Router()
router.message.filter(ChatTypeFilter(['private']))


@router.message(CommandStart())
async def start_cmd(
        message: Message,
        i18n: dict[str, str],
        session: AsyncSession
):
    """Handles command `/start`"""

    main_page = await orm_get_info_page(session, page_name='main')

    await message.answer_photo(
        photo=main_page.image,
        caption=i18n['main'],
        reply_markup=main_menu_keyboard(i18n)
    )


@router.callback_query(AddProductToCartCallback.filter())
async def add_product_to_cart(
        query: CallbackQuery,
        callback_data: AddProductToCartCallback,
        i18n: dict[str, Any],
        session: AsyncSession
):
    """Handles adding product to cart."""

    await orm_add_to_cart(
        session,
        callback_data.user_id,
        callback_data.product_id
    )
    await query.answer(i18n['add_to_cart_success'], show_alert=True)


@router.callback_query(PageCallbackFactory.filter(F.name == 'main'))
async def process_main_page(
        query: CallbackQuery,
        i18n: dict[str, Any],
        session: AsyncSession
):
    """Handles `main` page query by button."""

    await query.answer()
    main_page = await orm_get_info_page(session, page_name='main')

    await query.message.edit_media(
        media=InputMediaPhoto(media=main_page.image, caption=i18n['main']),
        reply_markup=main_menu_keyboard(i18n)
    )


@router.callback_query(PageCallbackFactory.filter(F.name == 'catalog'))
async def process_catalog_page(
        query: CallbackQuery,
        i18n: dict[str, Any],
        session: AsyncSession
):
    """Handles `catalog` button to retrieve catalog page."""

    await query.answer()

    catalog_page = await orm_get_info_page(session, page_name='catalog')
    categories = await orm_get_categories(session)

    await query.message.edit_media(
        media=InputMediaPhoto(media=catalog_page.image, caption=i18n['catalog']),
        reply_markup=catalog_page_keyboard(i18n, categories)
    )


@router.callback_query(or_f(
    CategoryCallbackFactory.filter(),
    PaginationCallbackFactory.filter()
))
async def process_products_list(
        query: CallbackQuery,
        callback_data: CategoryCallbackFactory | PaginationCallbackFactory,
        i18n: dict[str, Any],
        session: AsyncSession
):
    """Handles list of products by category."""

    await query.answer()
    user_id = query.from_user.id
    products = await orm_get_products(session, callback_data.category_id)

    if hasattr(callback_data, 'page'):
        page = callback_data.page
    else:
        page = 1

    paginator = Paginator(products, page=page)
    product = paginator.array[page-1]

    prev_page = page - 1 if paginator.has_prev() else None
    next_page = page + 1 if paginator.has_next() else None

    await query.message.edit_media(
        media=InputMediaPhoto(
            media=product.image,
            caption=f'<strong>{product.name}</strong>\n'
                    f'{product.description}\n'
                    f'{i18n['price']}: {round(product.price, 2)} {i18n['currency']}\n'
                    f'<strong>{i18n['item_word']} {paginator.page} '
                    f'{i18n['from_word']} {paginator.total_pages}</strong>',
            ),
        reply_markup=product_list_keyboard(
            i18n=i18n,
            category_id=callback_data.category_id,
            product=product,
            user_id=user_id,
            prev_page=prev_page,
            next_page=next_page
        )
    )



@router.message(or_f(Command('about'), ReplyButtonsFilter('about')))
async def about_cmd(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n['/about'])


@router.message(or_f(Command('payment'), ReplyButtonsFilter('payment')))
async def payment_cmd(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n['/payment'])


@router.message(
    F.text.lower().regexp(r'.*варианты? доставки.*') |
    F.text.lower().contains('доставк')
)
@router.message(or_f(Command('shipping'), ReplyButtonsFilter('shipping')))
async def shipping_cmd(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n['/shipping'])
