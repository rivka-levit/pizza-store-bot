from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(text='Привет, я виртуальный помощник.')


@router.message(Command('start'))
async def menu_cmd(message: Message):
    await message.answer(text='Вот меню:')
