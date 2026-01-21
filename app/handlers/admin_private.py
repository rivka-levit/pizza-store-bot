import logging
from typing import Any

from aiogram import Router
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import ObjectDeletedError, NoResultFound

from callbacks import DeleteProductCallbackFactory
from database.orm_query import orm_get_products, orm_delete_product

from filters.chat_types import ChatTypeFilter
from filters.reply_buttons import ReplyButtonsFilter
from filters.text_filters import TextEqualFilter
from filters.user_role import IsAdmin

from keyboards.inline_keyboards import get_edit_product_keyboard
from keyboards.reply_keyboards import get_admin_keyboard

logger = logging.getLogger(__name__)

router = Router()
router.message.filter(ChatTypeFilter(['private']), IsAdmin())


@router.message(Command('admin'))
async def admin_cmd(message: Message, i18n: dict[str, str | Any]) -> None:
    await message.answer(
        text=i18n['/admin'],
        reply_markup=get_admin_keyboard(i18n=i18n)
    )


@router.message(
    StateFilter('*'),
    or_f(Command('cancel'), TextEqualFilter('cancel_fsm'))
)
async def cancel_cmd(
        message: Message,
        i18n: dict[str, str | Any],
        state: FSMContext
) -> None:
    """Cancel any FSM dialog and clear state."""

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    logger.info('Add item process cancelled.')

    await message.answer(
        text=i18n['/cancel'],
        reply_markup=get_admin_keyboard(i18n=i18n)
    )


@router.message(ReplyButtonsFilter('catalog'))
async def products_catalog(
        message: Message,
        i18n: dict[str, str | Any],
        session: AsyncSession
) -> None:
    await message.answer(text=i18n['catalog_answer'])
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f'<strong>{product.name}</strong>\n{product.description}\n'
                    f'{i18n['price']}: {round(product.price, 2)} {i18n['currency']}',
            reply_markup=get_edit_product_keyboard(product, i18n)
        )


@router.callback_query(DeleteProductCallbackFactory.filter())
async def delete_product_btn_clicked(
        query: CallbackQuery,
        callback_data: DeleteProductCallbackFactory,
        i18n: dict[str, Any],
        session: AsyncSession
) -> None:
    """Delete product from database."""

    try:
        await orm_delete_product(session, callback_data.product_id)
    except (ObjectDeletedError, NoResultFound) as e:
        logger.error(
            f'{e.__class__.__name__}: Product with id '
            f'{callback_data.product_id} was not found.'
        )
        await query.answer()
        await query.message.answer(text=i18n['product_not_exists'])
    except Exception as e:
        logger.error(e)
        await query.answer()
    else:
        logger.info(
            f'Product {callback_data.product_name} with id '
            f'`{callback_data.product_id}` deleted successfully.'
        )
        await query.answer()
        await query.message.answer(
            text=i18n['product_deleted'].format(callback_data.product_name)
        )
