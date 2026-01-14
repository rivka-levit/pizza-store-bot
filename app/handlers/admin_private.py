from typing import Any

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

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


# Code for Finite State Machine (FSM)

@router.message(ReplyButtonsFilter('add_item'))
async def add_item_btn_clicked(
        message: Message,
        i18n: dict[str, str | Any]
) -> None:
    await message.answer(
        text=i18n['add_product_name'],
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command('cancel'))
async def cancel_cmd(message: Message, i18n: dict[str, str | Any]) -> None:
    await message.answer(
        text=i18n['/cancel'],
        reply_markup=get_admin_keyboard(i18n=i18n)
    )


@router.message(Command('back'))
async def back_cmd(message: Message, i18n: dict[str, str | Any]) -> None:
    await message.answer(text=i18n['/back'])


@router.message(F.text)
async def add_product_name(message: Message, i18n: dict[str, str | Any]) -> None:
    await message.answer(text=i18n['add_product_description'])


@router.message(F.text)
async def add_product_description(message: Message, i18n: dict[str, str | Any]) -> None:
    await message.answer(text=i18n['add_product_price'])


@router.message(F.text)
async def add_product_price(message: Message, i18n: dict[str, str | Any]) -> None:
    await message.answer(text=i18n['add_product_image'])


@router.message(F.text)
async def add_product_image(message: Message, i18n: dict[str, str | Any]) -> None:
    await message.answer(
        text=i18n['item_added'],
        reply_markup=get_admin_keyboard(i18n=i18n)
    )
