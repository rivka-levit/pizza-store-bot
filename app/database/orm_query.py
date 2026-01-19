from collections.abc import Sequence
from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Product


async def orm_add_product(session: AsyncSession, data: dict[str, Any]) -> None:
    """Add product to database"""

    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=float(data['price']),
        image=data['image']
    )
    session.add(new_product)
    await session.commit()


async def orm_get_products(session: AsyncSession) -> Sequence[Product]:
    """Get all the products from database"""

    query = select(Product)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_product(session: AsyncSession, product_id: int) -> Product:
    """Get one product from database"""

    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    return result.scalars().one()


async def orm_update_product(
        session: AsyncSession,
        product_id: int,
        data: dict[str, Any]
) -> None:
    """Update product in database"""

    query = update(Product).where(Product.id == product_id).values(
        name=data['name'],
        description=data['description'],
        price=float(data['price']),
        image=data['image']
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_product(session: AsyncSession, product_id: int) -> None:
    """Delete product from database"""

    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    await session.commit()
