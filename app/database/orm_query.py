from collections.abc import Sequence
from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from database.models import Product, InfoPage, Category, User


# ===================== Banners (info pages) ============================

async def orm_add_info_pages(session: AsyncSession, pages: list[str]) -> None:
    query = select(InfoPage)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all(
        [InfoPage(name=name) for name in pages]
    )
    await session.commit()


async def orm_change_page_image(
        session: AsyncSession,
        name: str,
        image: str
) -> None:
    query = update(InfoPage).where(InfoPage.name == name).values(image=image)
    await session.execute(query)
    await session.commit()


async def orm_get_info_page(session: AsyncSession, page_name: str) -> InfoPage:
    query = select(InfoPage).where(InfoPage.name == page_name)
    result = await session.execute(query)
    return result.scalars().first()


async def orm_get_info_pages(session: AsyncSession) -> Sequence[InfoPage]:
    query = select(InfoPage)
    result = await session.execute(query)
    return result.scalars().all()

# =========================== Categories ================================

async def orm_get_categories(session: AsyncSession) -> Sequence[Category]:
    """Return all the categories from database"""

    query = select(Category)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_create_categories(session: AsyncSession, categories: list[str]):
    """Create categories if not exist."""

    query = select(Category)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Category(name=name) for name in categories])
    await session.commit()

# ========================== Admin Panel ================================

async def orm_add_product(session: AsyncSession, data: dict[str, Any]):
    """Add product to database"""

    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=float(data['price']),
        image=data['image'],
        category_id=data['category_id']
    )
    session.add(new_product)
    await session.commit()


async def orm_get_products(session: AsyncSession, category_id: int) -> Sequence[Product]:
    """Get all the products from database"""

    query = select(Product).where(Product.category_id == category_id)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_product(session: AsyncSession, product_id: int) -> Product:
    """Get one product from database"""

    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    return result.scalars().one_or_none()


async def orm_update_product(
        session: AsyncSession,
        product_id: int | Mapped[int],
        data: dict[str, Any]
) -> None:
    """Update product in database"""

    query = update(Product).where(Product.id == product_id).values(
        name=data['name'],
        description=data['description'],
        price=float(data['price']),
        image=data['image'],
        category_id=data['category_id']
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_product(session: AsyncSession, product_id: int) -> None:
    """Delete product from database"""

    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    await session.commit()

# ========================== Add user to db ================================

async def orm_add_user(
        session: AsyncSession,
        tg_user_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None
):
    """Add user to database if not exists."""

    query = select(User).where(User.tg_id == tg_user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(User(
            tg_id=tg_user_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        ))
        await session.commit()
