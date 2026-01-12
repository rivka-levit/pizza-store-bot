from typing import Any

from aiogram.utils.formatting import as_list, as_marked_section, Bold

RU: dict[str, str | Any] = {
    '/start': 'Привет, я виртуальный помощник 👨‍💻',
    '/help': 'Бот помогает заказать пиццу 🍕',
    '/menu': '<b>Вот меню:</b>',
    '/about': '<b>О нас:</b>',
    '/payment': as_marked_section(
        Bold('Варианты оплаты:'),
        'Картой в боте',
        'При получении карта/кэш',
        'В заведении',
        marker='✅ '
    ).as_html(),
    '/shipping': as_list(
        as_marked_section(
            Bold('Варианты доставки/заказа:'),
            'Курьер',
            'Самовывоз (сейчас прибегу заберу)',
            'Покушаю у Вас (сейчас прибегу)',
            marker='✅ '
        ),
        as_marked_section(
            Bold('Нельзя:'),
            'Почта',
            'Голуби',
            marker='❌ '
        ),
        sep='\n------------------\n'
    ).as_html(),
    'start_description': 'Перезапустить бота',
    'help_description': 'Справка по работе бота',
    'menu_description': 'Меню пиццерии',
    'about_description': 'О нас',
    'payment_description': 'Оплата',
    'shipping_description': 'Доставка',
    'restricted_words': {'кабан', 'хомяк', 'выхухоль'},
    'btn_menu': 'Меню',
    'btn_about': 'О магазине',
    'btn_payment': 'Оплата',
    'btn_shipping': 'Доставка',
    'input_field_placeholder': 'Что Вас интересует?'
}
