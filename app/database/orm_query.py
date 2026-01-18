from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Product


async def orm_add_product(session: AsyncSession, data: dict[str, Any]):
    """Add product to database"""

    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=float(data['price']),
        image=data['image']
    )
    session.add(new_product)
    await session.commit()
