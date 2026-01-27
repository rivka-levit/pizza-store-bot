"""
Handlers for editing items Finite State Machine (FSM)
"""

import logging
from typing import Any

from aiogram import Router
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_product, orm_update_product

from callbacks import EditProductCallbackFactory

from filters.chat_types import ChatTypeFilter
from filters.text_filters import TextEqualFilter
from filters.user_role import IsAdmin

from handlers.utils import make_step_back

from keyboards.reply_keyboards import get_admin_keyboard
from states import EditItem

logger = logging.getLogger(__name__)

router = Router()
router.message.filter(
    ChatTypeFilter(['private']),
    IsAdmin(),
    ~TextEqualFilter('cancel_fsm')
)


@router.callback_query(StateFilter(None), EditProductCallbackFactory.filter())
async def edit_item_btn_clicked(
        callback: CallbackQuery,
        callback_data: EditProductCallbackFactory,
        i18n: dict[str, Any],
        session: AsyncSession,
        state: FSMContext
):
    """Start editing a product. Request the name."""

    product = await orm_get_product(session, int(callback_data.product_id))

    EditItem.product_to_edit = product

    await callback.answer()
    await callback.message.answer(
        text=i18n['edit_product_name'],
        reply_markup=ReplyKeyboardRemove()
    )
    logger.info('Edit item process started.')
    await state.set_state(EditItem.name)


@router.message(StateFilter(EditItem), or_f(Command('back'), TextEqualFilter('back_fsm')))
async def back_cmd(
        message: Message,
        i18n: dict[str, str | Any],
        state: FSMContext,
        edit_item_texts: dict[str, str]
) -> None:
    """Handles `/back` command in FSM dialog when adding a product."""

    current_state = await state.get_state()
    if current_state is None:
        return

    await make_step_back(
        state_group=EditItem,
        message=message,
        i18n=i18n,
        state=state,
        edit_item_texts=edit_item_texts,
        current_state=current_state
    )


@router.message(StateFilter(EditItem.name))
async def edit_item_name(
        message: Message,
        i18n: dict[str, str | Any],
        state: FSMContext
) -> None:
    """Edit product name in database or skip the step."""

    if not message.text:
        logger.warning('Wrong data received at the name step.')
        await message.answer(
            text=f'{i18n['wrong_data_received']}\n{i18n['edit_product_name']}'
        )
    elif message.text == '.':
        await state.update_data(name=EditItem.product_to_edit.name)
        await message.answer(i18n['edit_product_description'])
        await state.set_state(EditItem.description)
    else:
        await state.update_data(name=message.text)
        await message.answer(text=i18n['edit_product_description'])
        await state.set_state(EditItem.description)


@router.message(StateFilter(EditItem.description))
async def edit_item_description(
        message: Message,
        i18n: dict[str, str | Any],
        state: FSMContext
) -> None:
    """Edit product description in database or skip the step."""

    if not message.text:
        logger.warning('Wrong data received at the name step.')
        await message.answer(
            text=f'{i18n['wrong_data_received']}\n{i18n['edit_product_description']}'
        )
    elif message.text == '.':
        await state.update_data(description=EditItem.product_to_edit.description)
        await message.answer(i18n['edit_product_price'])
        await state.set_state(EditItem.price)
    else:
        await state.update_data(description=message.text)
        await message.answer(text=i18n['edit_product_price'])
        await state.set_state(EditItem.price)


@router.message(StateFilter(EditItem.price))
async def edit_item_price(
        message: Message,
        i18n: dict[str, str | Any],
        state: FSMContext
) -> None:
    """Edit product price in database or skip the step."""

    if not message.text:
        logger.warning('Wrong data received at the name step.')
        await message.answer(
            text=f'{i18n['wrong_data_received']}\n{i18n['edit_product_price']}'
        )
    elif message.text == '.':
        await state.update_data(price=EditItem.product_to_edit.price)
        await message.answer(i18n['edit_product_image'])
        await state.set_state(EditItem.image)
    else:
        await state.update_data(price=message.text)
        await message.answer(text=i18n['edit_product_image'])
        await state.set_state(EditItem.image)


@router.message(StateFilter(EditItem.image))
async def edit_item_image(
        message: Message,
        i18n: dict[str, str | Any],
        session: AsyncSession,
        state: FSMContext
) -> None:
    """Edit product image in database."""

    if not message.photo and not (message.text and message.text == '.'):
        logger.warning('Wrong data received at the image step.')
        await message.answer(
            text=f'{i18n['wrong_data_received']}\n{i18n['edit_product_image']}'
        )
        return

    if message.text and message.text == '.':
        await state.update_data(image=EditItem.product_to_edit.image)
    elif message.photo:
        await state.update_data(image=message.photo[-1].file_id)

    product_id = EditItem.product_to_edit.id
    data = await state.get_data()

    try:
        await orm_update_product(session, product_id, data)
    except Exception as e:
        logger.exception(f'Edit item process failed. Database error: {e}')
        await message.answer(
            text=i18n['add_db_error'].format(str(e)),
            reply_markup=get_admin_keyboard(i18n=i18n)
        )
    else:
        logger.info('Edit item process finished.')
        await message.answer(
            text=i18n['edit_db_success'],
            reply_markup=get_admin_keyboard(i18n=i18n)
        )
    finally:
        await state.clear()
        EditItem.product_to_edit = None
