from aiogram import Dispatcher
from aiogram import types

async def aaaa(message: types.Message):
    await message.answer('helloooo')



def register_all_handlers_db(dp: Dispatcher):
    dp.register_message_handler(aaaa, commands='dog')