from aiogram.filters.callback_data import CallbackData

from utils.pagination import Paginator


class AddProductToCartCallback(CallbackData, prefix='cart_add'):
    product_id: int
    user_id: int


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


class PaginationCallbackFactory(CallbackData, prefix='pagination'):
    page: int
