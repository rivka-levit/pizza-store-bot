import logging
from collections.abc import Sequence
from typing import Any

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from sqlalchemy.ext.asyncio import AsyncSession

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
