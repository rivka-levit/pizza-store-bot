import logging
from collections.abc import Sequence
from typing import Any

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession

from callbacks import PageCallbackFactory

from database.models import InfoPage
from database.orm_query import orm_get_info_pages

from filters.chat_types import ChatTypeFilter
from filters.reply_buttons import ReplyButtonsFilter
from filters.text_filters import TextEqualFilter
from filters.user_role import IsAdmin

from keyboards.inline_keyboards import page_choice_keyboard

from states import AddBanner

logger = logging.getLogger(__name__)

router = Router()
router.message.filter(
    ChatTypeFilter(['private']),
    IsAdmin(),
    ~TextEqualFilter('cancel_fsm')
)


@router.message(StateFilter(None), ReplyButtonsFilter('add_edit_banner'))
async def add_edit_banner(
        message: Message,
        i18n: dict[str, Any],
        state: FSMContext,
        session: AsyncSession
):
    pages: Sequence[InfoPage] = await orm_get_info_pages(session)

    await message.answer(
        text=i18n['choose_page_text'],
        reply_markup=page_choice_keyboard(
            pages=sorted(pages, key=lambda page: page.id),
            i18n=i18n
        ),
    )
    await state.set_state(AddBanner.page_id)


@router.callback_query(StateFilter(AddBanner.page_id), PageCallbackFactory.filter())
async def choose_page_step(
        query: CallbackQuery,
        callback_data: PageCallbackFactory,
        i18n: dict[str, Any],
        state: FSMContext,
):
    """Handles choice page button has been clicked."""

    await query.answer()
    await state.update_data(page_id=callback_data.id)
    await state.set_state(AddBanner.image)
    await query.message.edit_text(text=i18n['add_banner_image'])


@router.message(StateFilter(AddBanner.page_id))
async def wrong_page_data(message: Message, i18n: dict[str, Any]):
    """Handles wrong message on page choice step."""

    await message.answer(text=i18n['wrong_data_received'])
    return
