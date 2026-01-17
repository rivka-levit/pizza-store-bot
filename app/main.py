import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from redis.asyncio import Redis  # noqa

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from config import Config, load_config
from database.models import Base

from handlers.admin_add_item import router as admin_add_item_router
from handlers.admin_private import router as admin_private_router
from handlers.user_group import router as user_group_router
from handlers.user_private import router as user_private_router

from i18n.translator import get_translations

from middlewares.add_item_step_texts import AddItemStepTexts
from middlewares.i18n import TranslatorMiddleware

logger = logging.getLogger(__name__)


config_file: Config = load_config()


async def on_startup(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def on_shutdown():
    pass


async def main(config: Config):
    logging.basicConfig(
        level=logging.getLevelName(config.log.level),
        format=config.log.format,
        stream=config.log.stream
    )

    db_url = (f'postgresql+asyncpg://{config.db.user}:{config.db.password}'
              f'@{config.db.host}/{config.db.name}')

    engine = create_async_engine(db_url, echo=True)

    session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
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
    bot.admin_ids = config.bot.admin_ids
    dp = Dispatcher(storage=storage)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Register middlewares
    logger.info('Including middlewares...')
    dp.update.middleware(TranslatorMiddleware())
    admin_add_item_router.message.middleware(AddItemStepTexts())

    # Register routers
    dp.include_routers(
        admin_add_item_router,
        admin_private_router,
        user_private_router,
        user_group_router
    )

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
            engine=engine,
            db_pool=session_maker,
        )
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    asyncio.run(main(config_file))
