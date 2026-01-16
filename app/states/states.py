from aiogram.fsm.state import State, StatesGroup


class AddItem(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()
