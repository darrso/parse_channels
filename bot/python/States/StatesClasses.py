from aiogram.dispatcher.filters.state import State, StatesGroup


class Adding(StatesGroup):
    first = State()
    second = State()


class Removing(StatesGroup):
    first = State()
    second = State()

class Broadcast(StatesGroup):
    first = State()
    second = State()