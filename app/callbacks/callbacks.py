from aiogram.filters.callback_data import CallbackData

from utils.pagination import Paginator


class AddProductToCartCallback(CallbackData, prefix='cart_add'):
    product_id: int
    user_id: int


class CartManagingCallback(CallbackData, prefix='cart'):
    action: str
    user_id: int
    product_id: int


class CategoryCallbackFactory(CallbackData, prefix='cat'):
    category_id: int


class DeleteProductCallbackFactory(CallbackData, prefix='del'):
    product_id: int
    product_name: str


class EditProductCallbackFactory(CallbackData, prefix='edit'):
    product_id: int
    product_name: str


class PageCallbackFactory(CallbackData, prefix='page'):
    name: str


class PaginationCallbackFactory(CallbackData, prefix='pagination'):
    page: int
    category_id: int
