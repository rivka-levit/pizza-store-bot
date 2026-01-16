from typing import Any

from aiogram.utils.formatting import as_list, as_marked_section, Bold

RU: dict[str, str | Any] = {
    '/admin': 'Что хотите сделать?',
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
    '/cancel': 'Действия отменены',
    '/back': 'Oк, вы вернулись к прошлому шагу',
    'cansel_fsm': {'q', 'отмена', 'выход'},
    'back_fsm': {'b', 'back', 'назад'},
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
    'input_field_placeholder': 'Что Вас интересует?',
    'btn_add_item': 'Добавить товар',
    'btn_edit_item': 'Изменить товар',
    'btn_del_item': 'Удалить товар',
    'btn_just_looking': 'Я так, просто смотрю',
    'placeholder_admin_kb': 'Выберите действие...',
    'just_looking_answer': 'ОК, вот список товаров',
    'edit_item_answer': 'Выберите товар, который хотите изменить',
    'del_item_answer': 'Выберите товар(ы) для удаления',
    'add_product_name': 'Введите название товара',
    'add_product_description': 'Введите описание товара',
    'add_product_price': 'Введите стоимость товара',
    'add_product_image': 'Загрузите изображение товара',
    'item_added': 'Товар добавлен',
}
