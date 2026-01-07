import logging

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

logger = logging.getLogger(__name__)


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        """Find user language and put appropriate translation in data"""

        user: User = data.get('event_from_user')
        if user is None:
            return await handler(event, data)

        user_lang = user.language_code
        translations: dict = data.get('translations')
        i18n: dict = translations.get(user_lang)

        if i18n is None:
            data['i18n'] = translations[translations['default']]
        else:
            data['i18n'] = i18n

        return await handler(event, data)
