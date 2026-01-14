import logging
import os
import sys

from dataclasses import dataclass
from io import TextIOWrapper

from dotenv import find_dotenv, load_dotenv


logger = logging.getLogger(__name__)


@dataclass
class BotConfig:
    token: str
    admin_ids: list[int]
    allowed_updates: list[str]


@dataclass
class DatabaseConfig:
    name: str
    host: str
    port: int
    user: str
    password: str


@dataclass
class RedisConfig:
    host: str
    port: int
    db: int
    password: str
    username: str


@dataclass
class LogConfig:
    level: str
    format: str
    stream: TextIOWrapper | None = None


@dataclass
class Config:
    bot: BotConfig
    db: DatabaseConfig
    redis: RedisConfig
    log: LogConfig


def load_config(path: str | None = None) -> Config:
    if path:
        if not os.path.exists(path):
            logger.warning(".env file not found at '%s', skipping...", path)
            load_dotenv(find_dotenv())
        else:
            logger.info("Loading .env from '%s'", path)
            load_dotenv(find_dotenv(filename=path))
    else:
        load_dotenv(find_dotenv())

    token = os.environ.get('BOT_TOKEN')
    if not token:
        logger.error('`BOT_TOKEN` value is empty in .env file')
        raise ValueError('BOT_TOKEN must not be empty')

    bot = BotConfig(
        token=token,
        admin_ids=[int(i) for i in os.environ.get('ADMIN_IDS').split(',')],
        allowed_updates=os.environ.get('ALLOWED_UPDATES').split(',')
    )

    db = DatabaseConfig(
        name=os.environ.get('POSTGRES_DB'),
        host=os.environ.get('POSTGRES_HOST'),
        port=int(os.environ.get('POSTGRES_PORT')),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
    )

    redis = RedisConfig(
        host=os.environ.get('REDIS_HOST'),
        port=int(os.environ.get('REDIS_PORT')),
        db=int(os.environ.get('REDIS_DATABASE')),
        password=os.environ.get('REDIS_PASSWORD', default=''),
        username=os.environ.get('REDIS_USERNAME', default='')
    )

    log_settings = LogConfig(
        level=os.environ.get('LOG_LEVEL'),
        format=os.environ.get('LOG_FORMAT'),
        stream=sys.stdout
    )

    logger.info('Configuration loaded successfully')

    return Config(
        bot=bot,
        db=db,
        redis=redis,
        log=log_settings
    )
