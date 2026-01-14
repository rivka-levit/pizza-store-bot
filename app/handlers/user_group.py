from string import punctuation
from typing import Any

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from filters.chat_types import ChatTypeFilter

router = Router()
router.message.filter(ChatTypeFilter(['group', 'supergroup']))


def clean_text(text: str) -> str:
    return text.translate(str.maketrans('', '', punctuation))


@router.message(Command('set_admins'))
async def set_bot_admins(message: Message, bot: Bot) -> None:
    """Set admins list to bot attribute."""

    admins_list = await bot.get_chat_administrators(message.chat.id)

    admin_ids = {
        member.user.id for member in admins_list
        if (member.status == 'creator' or member.status == 'administrator')
           and member.user.id != bot.id
    }

    if message.from_user.id in admin_ids:
        bot.admin_ids.update(admin_ids)  # noqa
        await message.delete()



@router.edited_message()
@router.message()
async def clean_restricted_msg(message: Message, i18n: dict[str, str | Any]):
    """Handles deleting messages with restricted words."""

    normalized_words = clean_text(message.text.lower()).split()

    if i18n['restricted_words'].intersection(normalized_words):
        await message.answer(
            f'{message.from_user.first_name}, соблюдайте порядок в чате!'
        )
        await message.delete()
