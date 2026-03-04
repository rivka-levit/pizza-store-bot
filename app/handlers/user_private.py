from typing import Any

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, or_f
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from sqlalchemy.ext.asyncio import AsyncSession

from callbacks import PageCallbackFactory

from database.orm_query import (
    orm_get_categories,
    orm_get_info_page,
    orm_get_products
)

from filters.chat_types import ChatTypeFilter
from filters.reply_buttons import ReplyButtonsFilter

from keyboards.inline_keyboards import catalog_page_keyboard, main_menu_keyboard

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


# @router.message(ReplyButtonsFilter('menu'))
# @router.message(or_f(Command('menu'), F.text.lower().contains('меню')))
# async def menu_cmd(message: Message, i18n: dict[str, Any], session: AsyncSession):
#     await message.answer(text=i18n['/menu'])
#     for product in await orm_get_products(session):
#         await message.answer_photo(
#             product.image,
#             caption=f'<strong>{product.name}</strong>\n{product.description}\n'
#                     f'{i18n['price']}: {product.price:.2f} {i18n['currency']}'
#         )


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
