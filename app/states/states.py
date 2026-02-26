from aiogram.fsm.state import State, StatesGroup

from database.models import Product


class AddItem(StatesGroup):
    name = State()
    category = State()
    description = State()
    price = State()
    image = State()


class EditItem(StatesGroup):
    name = State()
    category = State()
    description = State()
    price = State()
    image = State()

    product_to_edit: Product | None = None


class AddBanner(StatesGroup):
    page_id = State()
    image = State()
