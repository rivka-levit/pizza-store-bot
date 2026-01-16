import logging

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class AddItemStepTexts(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        """Create and pass to data all steps` texts for AddItem dialog."""

        i18n = data['i18n']
        texts = {
                'AddItem:name': f'{i18n['add_product_name']}',
                'AddItem:description': f'{i18n['add_product_description']}',
                'AddItem:price': f'{i18n['add_product_price']}',
                'AddItem:image': f'{i18n['add_product_image']}'
        }
        data['add_item_texts'] = texts

        return await handler(event, data)
