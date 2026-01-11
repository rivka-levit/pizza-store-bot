from aiogram import Bot, F, Router
from aiogram.enums import BotCommandScopeType
from aiogram.filters import Command, CommandStart, or_f
from aiogram.types import Message, BotCommandScopeChat

from filters.chat_types import ChatTypeFilter
from keyboards.main_menu import get_main_menu_commands
from keyboards.reply import get_start_kb

router = Router()
router.message.filter(ChatTypeFilter(['private']))


@router.message(CommandStart())
async def start_cmd(message: Message, bot: Bot, i18n: dict[str, str]):
    await bot.set_my_commands(
        commands=get_main_menu_commands(i18n=i18n),
        scope=BotCommandScopeChat(
            type=BotCommandScopeType.CHAT,
            chat_id=message.chat.id
        )
    )
    await message.answer(
        text=i18n['/start'],
        reply_markup=get_start_kb(i18n=i18n)
    )


@router.message(Command('help'))
async def help_cmd(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n['/help'])


@router.message(or_f(Command('menu'), F.text.lower().contains('меню')))
async def menu_cmd(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n['/menu'])


@router.message(Command('about'))
async def about_cmd(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n['/about'])


@router.message(Command('payment'))
async def payment_cmd(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n['/payment'])


@router.message(
    F.text.lower().regexp(r'.*варианты? доставки.*') |
    F.text.lower().contains('доставк')
)
@router.message(Command('shipping'))
async def shipping_cmd(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n['/shipping'])
