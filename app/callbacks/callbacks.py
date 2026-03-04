from aiogram.filters.callback_data import CallbackData


class EditProductCallbackFactory(CallbackData, prefix='edit'):
    product_id: int
    product_name: str


class DeleteProductCallbackFactory(CallbackData, prefix='del'):
    product_id: int
    product_name: str


class CategoryCallbackFactory(CallbackData, prefix='cat'):
    category_id: int


class PageCallbackFactory(CallbackData, prefix='page'):
    name: str
