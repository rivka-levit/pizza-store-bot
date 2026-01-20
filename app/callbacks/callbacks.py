from aiogram.filters.callback_data import CallbackData


class EditProductCallbackFactory(CallbackData, prefix='edit'):
    product_id: int


class DeleteProductCallbackFactory(CallbackData, prefix='del'):
    product_id: int
