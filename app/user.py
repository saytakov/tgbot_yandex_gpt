import uuid
from decimal import Decimal

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message
from yandex_cloud_ml_sdk._exceptions import AioRpcError

import app.keyboards as kb
from app.database.requests import calculate, get_or_create_user
from app.generators import YaGPT_image, YaGPT_text
from app.states import Chat, Image

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Запуск чата."""
    await get_or_create_user(message.from_user.id)
    await message.answer('Здравствуйте!', reply_markup=kb.main)
    await state.clear()


@user.message(F.text == 'Отмена')
async def cmd_cancel(message: Message, state: FSMContext):
    """Обработка кнопки 'Отмена'"""
    await state.clear()
    await message.answer('Что Вы желаете сделать?', reply_markup=kb.main)


@user.message(Image.wait)
@user.message(Chat.wait)
async def chatting_wait(message: Message):
    """Ошибка ввода сообщения во время обработки запроса."""
    await message.answer(
        'Прошу прощения, я могу обрабатывать только одно сообщение за раз.'
    )


@user.message(F.text == 'Чат')
async def chatting(message: Message, state: FSMContext):
    """Обработка нажатия на кнопку 'Чат'"""
    user = await get_or_create_user(message.from_user.id)
    if user is None:
        await message.answer('Ошибка на сервере, попробуйте позже.')
        return
    if Decimal(user.balance) > 0 or True:  # Debug условие, в случае публикации убрать данное условие
        await state.set_state(Chat.text)
        await message.answer('Введите Ваш запрос.', reply_markup=kb.cancel)
    else:
        await message.answer('У вас недостаточно средств на счете.')


@user.message(Chat.text)
async def chatting_response_text(message: Message, state: FSMContext):
    """Отправка запроса к ИИ, возвращение результата пользователю."""
    user_id = message.from_user.id
    user = await get_or_create_user(user_id)
    if user is None:
        await message.answer('Ошибка на сервере, попробуйте позже.')
        return
    if Decimal(user.balance) > 0 or True:  # Debug условие, в случае публикации убрать данное условие
        await state.set_state(Chat.wait)
        message = await message.answer('Обрабатываю запрос...')
        response = await YaGPT_text(message.text, 'yandexgpt-lite')
        await calculate(user_id, response['total_tokens'], 'yandexgpt-lite')
        await message.delete()
        await message.answer(response['text'], parse_mode=ParseMode.MARKDOWN)
        await state.set_state(Chat.text)
    else:
        await message.answer('У вас недостаточно средств на счете.')


@user.message(F.text == 'Генерация картинок')
async def orientation_for_image(message: Message, state: FSMContext):
    """Обработка нажатия на кнопку 'Генерация картинок'"""
    user = await get_or_create_user(message.from_user.id)
    if user is None:
        await message.answer('Ошибка на сервере, попробуйте позже.')
        return
    if Decimal(user.balance) > 0 or True:  # Debug условие, в случае публикации убрать данное условие
        await state.set_state(Image.orientation)
        await message.answer(
            'Выберите ориентацию будущего изображения',
            reply_markup=kb.orientation
        )
    else:
        await message.answer('У вас недостаточно средств на счете.')


@user.message(Image.orientation)
async def request_for_image(message: Message, state: FSMContext):
    """Выбор формата картинки."""
    user = await get_or_create_user(message.from_user.id)
    if user is None:
        await message.answer('Ошибка на сервере, попробуйте позже.')
        return
    if Decimal(user.balance) > 0 or True:  # Debug условие, в случае публикации убрать данное условие
        await state.update_data(orientation=message.text)
        await state.set_state(Image.image)
        await message.answer('Введите Ваш запрос.', reply_markup=kb.cancel)
    else:
        await message.answer('У вас недостаточно средств на счете.')


@user.message(Image.image)
async def chatting_response_image(message: Message, state: FSMContext):
    """Отправка запроса к ИИ, возвращение результата пользователю."""
    user = await get_or_create_user(message.from_user.id)
    if user is None:
        await message.answer('Ошибка на сервере, попробуйте позже.')
        return
    if (Decimal(user.balance) > 0) or True:  # Debug условие, в случае публикации убрать данное условие
        await state.update_data(image=message.text)
        data = await state.get_data()
        await state.set_state(Image.wait)
        try:
            response = await YaGPT_image(
                req=data['image'],
                model_name='yandex-art',
                orientation=data['orientation']
            )
            await calculate(
                tg_id=message.from_user.id,
                total_tokens=response['total_tokens'],
                model_name='yandex-art'
            )
            file_name = uuid.uuid4()
            photo = BufferedInputFile(
                file=response['image'].image_bytes,
                filename=f'{file_name}.jpeg'
            )
            await message.answer_photo(photo=photo)

        except AioRpcError:
            await message.answer("Ваш запрос был введен некорретно, пожалуйста, попробуйте изменить описание изображения.")
        await state.set_state(Image.image)
    else:
        await message.answer('У вас недостаточно средств на счете.')
