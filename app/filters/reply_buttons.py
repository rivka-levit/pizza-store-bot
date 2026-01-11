from typing import Any

from aiogram.filters import Filter
from aiogram.types import Message


class ReplyButtonsFilter(Filter):
    def __init__(self, btn_name: str) -> None:
        self.btn_name = btn_name

    async def __call__(self, message: Message, i18n: dict[str, str | Any]):
        return i18n[f'btn_{self.btn_name}'].lower() == message.text.lower()
