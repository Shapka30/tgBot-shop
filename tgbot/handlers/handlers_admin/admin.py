from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.markdown import hcode

from tgbot.config import db
from tgbot.keyboards.inline import admin_menu, admin_products_menu


async def admin_start(message: types.Message, state: FSMContext):
    await message.answer(f'Здравствуйте {message.from_user.first_name}, вы являетесь администратором этого бота')
    await message.answer('Ваша панель управления', reply_markup=admin_menu)
    await state.finish()


async def admin_count_users(call: types.CallbackQuery):
    count_user = await db.count_users()
    await call.answer(f'Сейчас в базе данных находится {count_user} пользователя')


async def command_admin_products_menu(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text('Ваша панель управления товарами', reply_markup=admin_products_menu)


async def command_back_admin_menu(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.answer('Данные которые вы ввели при добавление товара не сохраняться', show_alert=True)
    await call.message.edit_text('Ваша панель управления', reply_markup=admin_menu)
    if await state.get_state() is None:
        return
    await state.finish()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, CommandStart(), state="*", is_admin=True)
    dp.register_callback_query_handler(admin_count_users, text='count users', is_admin=True)
    dp.register_callback_query_handler(command_admin_products_menu, text='products', is_admin=True)
    dp.register_callback_query_handler(command_back_admin_menu, text='back admin menu', state=['*'], is_admin=True)
