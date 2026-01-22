from aiogram.fsm.state import State, StatesGroup

from database.models import Product


class AddEditItem(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    product_to_edit: Product | None = None
