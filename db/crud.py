from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Product


async def crud_get_products(session: AsyncSession):
    query = select(Product)
    products = await session.execute(query)
    return products.scalars().all()


async def crud_get_product(session: AsyncSession, id: int):
    query = select(Product).where(Product.id == id)
    product = await session.execute(query)
    return product.scalars()


async def crud_add_product(session: AsyncSession, data: dict):
    session.add(Product(
        name=data["name"],
        description=data["description"],
        price=data["price"],
        image=data["image"],
    ))
    await session.commit()


async def crud_update_product(session: AsyncSession, id: int, data: dict):
    query = update(Product).where(Product.id == id).values(
        name=data["name"],
        description=data["description"],
        price=data["price"],
        image=data["image"],
    )
    await session.execute(query)
    await session.commit()


async def crud_delete_product(session: AsyncSession, id: int):
    query = delete(Product).where(Product.id == id)
    await session.execute(query)
    await session.commit()
