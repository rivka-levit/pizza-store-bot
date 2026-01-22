"""
Handlers for editing items Finite State Machine (FSM)
"""

import logging
from typing import Any

from aiogram import Router, F
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_product

from callbacks import EditProductCallbackFactory

from filters.chat_types import ChatTypeFilter
from filters.text_filters import TextEqualFilter
from filters.user_role import IsAdmin

from keyboards.reply_keyboards import get_admin_keyboard
from states import AddEditItem

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
        state: FSMContext
):
    """Start editing a product. Request the name."""

    AddEditItem.product_edit_id = callback_data.product_id

    await callback.answer()
    await callback.message.answer(
        text=i18n['edit_product_name'],
        reply_markup=ReplyKeyboardRemove()
    )
    logger.info('Edit item process started.')
    await state.set_state(AddEditItem.name)


@router.message(StateFilter(AddEditItem), or_f(Command('back'), TextEqualFilter('back_fsm')))
async def back_cmd(
        message: Message,
        i18n: dict[str, str | Any],
        state: FSMContext,
        edit_item_texts: dict[str, str]
) -> None:
    """Roll back FSM dialog one step backwards."""

    current_state = await state.get_state()
    if current_state is None:
        return
    if current_state == AddEditItem.name:
        await message.answer(i18n['no_prev_step'])
        return

    previous = None
    for step in AddEditItem.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                text=f"{i18n['/back']}\n{edit_item_texts[previous.state]}"
            )
            return
        previous = step


@router.message(StateFilter(AddEditItem.name), or_f(F.text, F.text=='.'))
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
        await message.answer(i18n['edit_product_description'])
        await state.set_state(AddEditItem.description)
    else:
        await state.update_data(name=message.text)
        await message.answer(text=i18n['edit_product_description'])
        await state.set_state(AddEditItem.description)


@router.message(StateFilter(AddEditItem.name), or_f(F.text, F.text=='.'))
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
        await message.answer(i18n['edit_product_price'])
        await state.set_state(AddEditItem.price)
    else:
        await state.update_data(description=message.text)
        await message.answer(text=i18n['edit_product_price'])
        await state.set_state(AddEditItem.price)
