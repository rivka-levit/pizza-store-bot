from typing import Any

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup

from filters.chat_types import ChatTypeFilter
from filters.reply_buttons import ReplyButtonsFilter
from filters.user_role import IsAdmin
from keyboards.reply_keyboards import reply_kb_factory

router = Router()
router.message.filter(ChatTypeFilter(['private']), IsAdmin())


def get_admin_keyboard(i18n: dict[str, str | Any]) -> ReplyKeyboardMarkup:
    buttons = [
        i18n['btn_add_item'],
        i18n['btn_edit_item'],
        i18n['btn_del_item'],
        i18n['btn_just_looking'],
    ]
    return reply_kb_factory(
        *buttons,
        placeholder=i18n['placeholder_admin_kb'],
        sizes=(2, 1, 1)
    )


@router.message(Command('admin'))
async def admin_cmd(message: Message, i18n: dict[str, str | Any]) -> None:
    await message.answer(
        text=i18n['/admin'],
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
