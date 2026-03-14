from aiogram import F, Router
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from app.database.requests import get_users
from app.states import NewsLetter

admin = Router()


class Admin(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [976850363, 456]


@admin.message(Admin(), Command('newsletter'))
async def newsletter(message: Message, state: FSMContext):
    await state.set_state(NewsLetter.message)
    await message.answer('Введите сообщение для расслыки:')


@admin.message(NewsLetter.message)
async def newsletter_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Рассылка началась.')
    users = await get_users()
    for user in users:
        try:
            await message.send_copy(chat_id=user.tg_id)
        except Exception as e:
            print(e)
    await message.answer('Рассылка завершена.')
