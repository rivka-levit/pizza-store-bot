from typing import Any, Type

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import AddItem, EditItem


async def make_step_back(
        state_group: Type[AddItem] | Type[EditItem],
        message: Message,
        i18n: dict[str, Any],
        state: FSMContext,
        edit_item_texts: dict[str, str],
        current_state: str
):
    """Rollback FSM dialog one step backwards."""

    if current_state == state_group.name:
        await message.answer(i18n['no_prev_step'])
        return

    previous = None
    for step in state_group.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            key = previous.state.split(':')[-1]
            await message.answer(
                text=f"{i18n['/back']}\n{edit_item_texts[key]}"
            )
            return
        previous = step
