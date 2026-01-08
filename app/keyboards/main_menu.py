from aiogram.types import BotCommand


def get_main_menu_commands(i18n: dict[str, str]) -> list[BotCommand]:
    """Returns a list of commands for main menu button."""

    return [
        BotCommand(
            command='/start',
            description=i18n.get('start_description')
        ),
        BotCommand(
            command='/help',
            description=i18n.get('help_description')
        ),
        BotCommand(
            command='/menu',
            description=i18n.get('menu_description')
        ),
        BotCommand(
            command='/about',
            description=i18n.get('about_description')
        ),
        BotCommand(
            command='/payment',
            description=i18n.get('payment_description')
        ),
        BotCommand(
            command='/shipping',
            description=i18n.get('shipping_description')
        )
    ]
