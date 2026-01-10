import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from config import Config, load_config
from redis.asyncio import Redis  # noqa

from handlers.other import router as other_router
from handlers.user_group import router as user_group_router
from handlers.user_private import router as user_private_router
from i18n.translator import get_translations
from middlewares.i18n import TranslatorMiddleware

logger = logging.getLogger(__name__)


async def main():
    config: Config = load_config()

    logging.basicConfig(
        level=logging.getLevelName(config.log.level),
        format=config.log.format,
        stream=config.log.stream
    )

    storage = RedisStorage(
        redis=Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
            password=config.redis.password,
            username=config.redis.username,
        )
    )


    # Initialize the bot
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    # Register routers
    dp.include_routers(
        user_private_router,
        user_group_router,
        other_router
    )

    # Register middlewares
    logger.info('Including middlewares...')
    dp.update.middleware(TranslatorMiddleware())

    # Translations
    translations = get_translations()
    locales = list(translations.keys())

    # Run polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot,
            allowed_updates=config.bot.allowed_updates,
            translations=translations,
            locales=locales,
        )
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    asyncio.run(main())
