from string import punctuation
from typing import Any

from aiogram import Router
from aiogram.types import Message

from filters.chat_types import ChatTypeFilter

router = Router()
router.message.filter(ChatTypeFilter(['group', 'supergroup']))


def clean_text(text: str) -> str:
    return text.translate(str.maketrans('', '', punctuation))


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
