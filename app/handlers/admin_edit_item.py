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

    await callback.message.answer(
        text=i18n['edit_product_name'],
        reply_markup=ReplyKeyboardRemove()
    )
    logger.info('Edit item process started.')
    await state.set_state(AddEditItem.name)
