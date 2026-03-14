from aiogram.fsm.state import State, StatesGroup


class Chat(StatesGroup):
    text = State()
    wait = State()


class Image(StatesGroup):
    orientation = State()
    image = State()
    wait = State()


class NewsLetter(StatesGroup):
    message = State()
