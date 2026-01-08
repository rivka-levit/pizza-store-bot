from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n['/start'])


@router.message(Command('help'))
async def help_cmd(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n['/help'])


@router.message(Command('menu'))
async def menu_cmd(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n['/menu'])


@router.message(Command('about'))
async def about_cmd(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n['/about'])


@router.message(Command('/payment'))
async def payment_cmd(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n['/payment'])


@router.message(Command('/shipping'))
async def shipping_cmd(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n['/shipping'])
