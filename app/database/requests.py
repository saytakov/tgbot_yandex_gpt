from decimal import Decimal

from app.database.models import AiModel, User, async_session
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(*args, session=session, **kwargs)
    return wrapper


@connection
async def get_or_create_user(tg_id: int, session: None | AsyncSession = None):
    if session is None:
        return
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        user = session.add(User(tg_id=tg_id, balance='0'))
        await session.commit()
    return user


@connection
async def get_users(session: None | AsyncSession = None):
    if session is None:
        return
    return await session.scalars(select(User))


@connection
async def calculate(
    tg_id: int,
    total_tokens: str,
    model_name: str,
    session: None | AsyncSession = None
):
    if session is None:
        return
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if user is None:
        return
    model = await session.scalar(
        select(AiModel)
        .where(AiModel.name == model_name)
    )
    if model is None:
        return
    new_balance = Decimal(
        Decimal(user.balance) - Decimal(total_tokens) * Decimal(model.price)
    )
    await session.execute(
        update(User)
        .where(User.id == user.id)
        .values(balance=str(new_balance))
    )
    await session.commit()
