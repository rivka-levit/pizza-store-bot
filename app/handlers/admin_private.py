import logging
from typing import Any

from aiogram import Router, F
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from filters.chat_types import ChatTypeFilter
from filters.reply_buttons import ReplyButtonsFilter
from filters.text_filters import TextEqualFilter
from filters.user_role import IsAdmin

from keyboards.reply_keyboards import reply_kb_factory
from states import AddItem

logger = logging.getLogger(__name__)

router = Router()
router.message.filter(ChatTypeFilter(['private']), IsAdmin())


def get_admin_keyboard(i18n: dict[str, str | Any]) -> ReplyKeyboardMarkup:
    buttons = [
        i18n['btn_add_item'],
        i18n['btn_edit_item'],
        i18n['btn_del_item'],
        i18n['btn_just_looking'],
    ]
    return reply_kb_factory(
        *buttons,
        placeholder=i18n['placeholder_admin_kb'],
        sizes=(2, 1, 1)
    )


@router.message(Command('admin'))
async def admin_cmd(message: Message, i18n: dict[str, str | Any]) -> None:
    await message.answer(
        text=i18n['/admin'],
        reply_markup=get_admin_keyboard(i18n=i18n)
    )


# ----------------- Code for Finite State Machine (FSM) ------------------

@router.message(StateFilter(None), ReplyButtonsFilter('add_item'))
async def add_item_btn_clicked(
        message: Message,
        i18n: dict[str, str | Any],
        state: FSMContext
) -> None:
    """Starting `add item` process. Request product name."""

    await message.answer(
        text=i18n['add_product_name'],
        reply_markup=ReplyKeyboardRemove()
    )

    logger.info('Add item process started.')
    await state.set_state(AddItem.name)


@router.message(
    StateFilter('*'),
    or_f(Command('cancel'), TextEqualFilter('cansel_fsm'))
)
async def cancel_cmd(
        message: Message,
        i18n: dict[str, str | Any],
        state: FSMContext
) -> None:
    """Cancel FSM dialog and clear state."""

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    logger.info('Add item process cancelled.')

    await message.answer(
        text=i18n['/cancel'],
        reply_markup=get_admin_keyboard(i18n=i18n)
    )


@router.message(StateFilter(AddItem), or_f(Command('back'), TextEqualFilter('back_fsm')))
async def back_cmd(
        message: Message,
        i18n: dict[str, str | Any],
        state: FSMContext,
        add_item_texts: dict[str, str]
) -> None:
    """Back FSM dialog one step backwards."""

    current_state = await state.get_state()
    if current_state is None:
        return
    if current_state == AddItem.name:
        await message.answer(
            'Предыдущего шага нет. Введите название товара или команду /cancel'
        )
        return

    previous = None
    for step in AddItem.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                text=f"{i18n['/back']}\n{add_item_texts[previous.state]}"
            )
            return
        previous = step


@router.message(AddItem.name, F.text)
async def add_product_name(
        message: Message, i18n:
        dict[str, str | Any],
        state: FSMContext
) -> None:
    """Add product name to state dictionary and request product description."""

    await state.update_data(name=message.text)
    await message.answer(text=i18n['add_product_description'])
    await state.set_state(AddItem.description)


@router.message(AddItem.description, F.text)
async def add_product_description(
        message: Message,
        i18n: dict[str, str | Any],
        state: FSMContext
) -> None:
    """Add product description to state dictionary and request product price."""

    await state.update_data(description=message.text)
    await message.answer(text=i18n['add_product_price'])
    await state.set_state(AddItem.price)


@router.message(AddItem.price, F.text)
async def add_product_price(
        message: Message, i18n:
        dict[str, str | Any],
        state: FSMContext
) -> None:
    """Add product price to state dictionary and request product image."""

    await state.update_data(price=message.text)
    await message.answer(text=i18n['add_product_image'])
    await state.set_state(AddItem.image)


@router.message(AddItem.image, F.photo)
async def add_product_image(
        message: Message,
        i18n: dict[str, str | Any],
        state: FSMContext
) -> None:
    """Add product image to state dictionary and quit fsm dialog."""

    await state.update_data(image=message.photo[-1].file_id)
    await message.answer(
        text=i18n['item_added'],
        reply_markup=get_admin_keyboard(i18n=i18n)
    )
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()
    logger.info('Add item process finished.')

# -------------------------- End FSM ----------------------------

@router.message(ReplyButtonsFilter('just_looking'))
async def just_looking_btn_clicked(
        message: Message,
        i18n: dict[str, str | Any]
) -> None:
    await message.answer(text=i18n['just_looking_answer'])


@router.message(ReplyButtonsFilter('edit_item'))
async def edit_item_btn_clicked(
        message: Message,
        i18n: dict[str, str | Any]
) -> None:
    await message.answer(text=i18n['edit_item_answer'])


@router.message(ReplyButtonsFilter('del_item'))
async def del_item_btn_clicked(
        message: Message,
        i18n: dict[str, str | Any]
) -> None:
    await message.answer(text=i18n['del_item_answer'])
