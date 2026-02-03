from collections.abc import Sequence
from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from database.models import Product, Banner, Category


# ===================== Banners (info pages) ============================

async def orm_add_banner_description(session: AsyncSession, data: dict) -> None:
    query = select(Banner)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all(
        [Banner(name=name, description=descr) for name, descr in data.items()]
    )
    await session.commit()


async def orm_change_banner_image(
        session: AsyncSession,
        name: str,
        image: str
) -> None:
    query = update(Banner).where(Banner.name == name).values(image=image)
    await session.execute(query)
    await session.commit()


async def orm_get_banner(session: AsyncSession, page_name: str) -> Banner:
    query = select(Banner).where(Banner.name == page_name)
    result = await session.execute(query)
    return result.scalars().first()


async def orm_get_info_pages(session: AsyncSession) -> Sequence[Banner]:
    query = select(Banner)
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
