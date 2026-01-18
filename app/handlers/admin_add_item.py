"""
Handlers for adding items Finite State Machine (FSM)
"""

import logging
from typing import Any

from aiogram import Router
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_product

from filters.chat_types import ChatTypeFilter
from filters.reply_buttons import ReplyButtonsFilter
from filters.text_filters import TextEqualFilter
from filters.user_role import IsAdmin

from keyboards.reply_keyboards import get_admin_keyboard
from states import AddItem

logger = logging.getLogger(__name__)

router = Router()
router.message.filter(
    ChatTypeFilter(['private']),
    IsAdmin(),
    ~TextEqualFilter('cancel_fsm')
)


@router.message(StateFilter(None), ReplyButtonsFilter('add_item'))
async def add_item_btn_clicked(
        message: Message,
        i18n: dict[str, str | Any],
        state: FSMContext
) -> None:
    """Starting `add item` process. Request product name."""

    await message.answer(
        text=i18n['add_product_name'],
        reply_markup=ReplyKeyboardRemove()
    )

    logger.info('Add item process started.')
    await state.set_state(AddItem.name)


@router.message(StateFilter(AddItem), or_f(Command('back'), TextEqualFilter('back_fsm')))
async def back_cmd(
        message: Message,
        i18n: dict[str, str | Any],
        state: FSMContext,
        add_item_texts: dict[str, str]
) -> None:
    """Back FSM dialog one step backwards."""

    current_state = await state.get_state()
    if current_state is None:
        return
    if current_state == AddItem.name:
        await message.answer(
            'Предыдущего шага нет. Введите название товара или команду /cancel'
        )
        return

    previous = None
    for step in AddItem.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                text=f"{i18n['/back']}\n{add_item_texts[previous.state]}"
            )
            return
        previous = step


@router.message(AddItem.name)
async def add_product_name(
        message: Message, i18n:
        dict[str, str | Any],
        state: FSMContext
) -> None:
    """Add product name to state dictionary and request product description."""

    if message.text:
        await state.update_data(name=message.text)
        await message.answer(text=i18n['add_product_description'])
        await state.set_state(AddItem.description)
    else:
        logger.warning('Wrong data received at the name step.')
        await message.answer(
            text=f'{i18n['wrong_data_received']}\n{i18n['add_product_name']}'
        )


@router.message(AddItem.description)
async def add_product_description(
        message: Message,
        i18n: dict[str, str | Any],
        state: FSMContext
) -> None:
    """Add product description to state dictionary and request product price."""

    if message.text:
        await state.update_data(description=message.text)
        await message.answer(text=i18n['add_product_price'])
        await state.set_state(AddItem.price)
    else:
        logger.warning('Wrong data received at the description step.')
        await message.answer(
            text=f'{i18n['wrong_data_received']}\n{i18n['add_product_description']}'
        )


@router.message(AddItem.price)
async def add_product_price(
        message: Message, i18n:
        dict[str, str | Any],
        state: FSMContext
) -> None:
    """Add product price to state dictionary and request product image."""

    if message.text:
        await state.update_data(price=message.text)
        await message.answer(text=i18n['add_product_image'])
        await state.set_state(AddItem.image)
    else:
        logger.warning('Wrong data received at the price step.')
        await message.answer(
            text=f'{i18n['wrong_data_received']}\n{i18n['add_product_price']}'
        )


@router.message(AddItem.image)
async def add_product_image(
        message: Message,
        i18n: dict[str, str | Any],
        state: FSMContext,
        session: AsyncSession
) -> None:
    """Add product image to state dictionary and quit fsm dialog."""

    if message.photo:
        await state.update_data(image=message.photo[-1].file_id)
        await message.answer(
            text=i18n['item_added'],
            reply_markup=get_admin_keyboard(i18n=i18n)
        )
        data = await state.get_data()

        try:
            await orm_add_product(session=session, data=data)
            logger.info('Add item process finished.')
            await message.answer(
                text=i18n['add_db_success'],
                reply_markup=get_admin_keyboard(i18n=i18n)
            )
            await state.clear()
        except Exception as e:
            logger.exception(f'Add item process failed. Database error: {e}')
            await message.answer(
                text=i18n['add_db_error'].format(str(e)),
                reply_markup=get_admin_keyboard(i18n=i18n)
            )
            await state.clear()

    else:
        logger.warning('Wrong data received at the image step.')
        await message.answer(
            text=f'{i18n['wrong_data_received']}\n{i18n['add_product_image']}'
        )
