from aiogram.filters import Filter
from aiogram.types import Message


class IsAdmin(Filter):
    async def __call__(self, message: Message, bot_admin_ids: list[int]) -> bool:
        return message.from_user.id in bot_admin_ids
