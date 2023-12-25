from aiogram.dispatcher.filters.state import State, StatesGroup

class editthisselectrepstate(StatesGroup):
    answer = State()

class addrepstates(StatesGroup):
    date = State()
    types = State()
    wtime = State()
    number = State()
    price = State()