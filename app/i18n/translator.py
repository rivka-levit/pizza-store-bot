from i18n.locales.ru.txt import RU


def get_translations() -> dict[str, str | dict[str, str]]:
    """Returns all the available translations in one dictionary."""

    return {
        'default': 'ru',
        'ru': RU,
    }
