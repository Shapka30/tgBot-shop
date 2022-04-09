from aiogram.dispatcher.filters.state import StatesGroup, State


class NewProduct(StatesGroup):
    name = State()
    photo = State()
    description = State()
    price = State()
    amount = State()
    article = State()
    confirm = State()


class Mailing(StatesGroup):
    text = State()
    confirm = State()


class DeleteProduct(StatesGroup):
    article = State()
    confirm = State()


class ChangePrice(StatesGroup):
    article = State()
    price = State()
    confirm = State()


class ChangeAmount(StatesGroup):
    article = State()
    amount = State()
    confirm = State()


class Buy(StatesGroup):
    amount = State()
    delivery = State()
    confirm = State()
