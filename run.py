import asyncio

import redis.asyncio as aioredis
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from app.admin import admin
from app.database.models import async_main
from app.user import user
from config import TOKEN_BOT


async def main():
    redis = await aioredis.from_url(f'redis://localhost:6379/0')
    storage=RedisStorage(redis)
    bot = Bot(token=TOKEN_BOT)
    dp = Dispatcher()
    dp.include_routers(user, admin)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


async def on_startup(dispatcher):
    await async_main()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
