import logging
from typing import Any

from aiogram import Router
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters.chat_types import ChatTypeFilter
from filters.reply_buttons import ReplyButtonsFilter
from filters.text_filters import TextEqualFilter
from filters.user_role import IsAdmin

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


@router.message(ReplyButtonsFilter('just_looking'))
async def just_looking_btn_clicked(
        message: Message,
        i18n: dict[str, str | Any]
) -> None:
    await message.answer(text=i18n['just_looking_answer'])


@router.message(ReplyButtonsFilter('edit_item'))
async def edit_item_btn_clicked(
        message: Message,
        i18n: dict[str, str | Any]
) -> None:
    await message.answer(text=i18n['edit_item_answer'])


@router.message(ReplyButtonsFilter('del_item'))
async def del_item_btn_clicked(
        message: Message,
        i18n: dict[str, str | Any]
) -> None:
    await message.answer(text=i18n['del_item_answer'])
