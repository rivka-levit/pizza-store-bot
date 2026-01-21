from aiogram.fsm.state import State, StatesGroup


class AddEditItem(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    product_edit_id = None
