import logging

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from sqlalchemy.ext.asyncio import async_sessionmaker

logger = logging.getLogger(__name__)


class DatabaseSessionMiddleware(BaseMiddleware):
    def __init__(self, db_pool: async_sessionmaker):
        self.db_pool = db_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        with self.db_pool() as session:
            try:
                data['session'] = session
                result = await handler(event, data)
            except Exception as e:
                logger.error('Transaction rolled back due to error: %s', e)
                raise

        return result
