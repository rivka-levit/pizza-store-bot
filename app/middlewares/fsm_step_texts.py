import logging

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class EditItemStepTexts(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        """Create and pass to data all steps` texts for edit item dialog."""

        i18n = data['i18n']
        texts = {
                'name': f'{i18n['edit_product_name']}',
                'description': f'{i18n['edit_product_description']}',
                'price': f'{i18n['edit_product_price']}',
                'image': f'{i18n['edit_product_image']}'
        }
        data['edit_item_texts'] = texts

        return await handler(event, data)
