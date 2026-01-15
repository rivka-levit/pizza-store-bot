from typing import Any

from aiogram.filters import Filter
from aiogram.types import Message


class TextEqualFilter(Filter):
    def __init__(self, text: str) -> None:
        self.text = text.casefold()

    async def __call__(self, message: Message, i18n: dict[str, Any]) -> bool:
        return self.text in i18n and message.text in i18n[self.text]
