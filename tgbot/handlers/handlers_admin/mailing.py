from asyncio import sleep

from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from tgbot.pop import db
from tgbot.keyboards.inline import admin_menu, back_admin_menu, chek_mailing_menu
from tgbot.misc.states import Mailing


async def create_mailing1(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text('Введите текст рассылки', reply_markup=back_admin_menu)
    await Mailing.text.set()


async def create_mailing2(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await message.answer(f'Так будет выглядить рассылка для пользователей:\n'
                         f'{text}', reply_markup=chek_mailing_menu)
    await Mailing.confirm.set()


async def create_mailing3(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    text = data['text']
    tg_users_id = list(await db.select_all_tg_users_id())

    for user in tg_users_id:
        try:
            await call.message.bot.send_message(chat_id=user[0], text=text)
            await sleep(0.2)
        except Exception:
            pass

    await call.message.answer('Рассылка выполнена')
    if await state.get_state() is None:
        return
    await state.finish()


async def change_mailing(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    if await state.get_state() is None:
        return
    await state.finish()
    await call.message.delete()
    await call.message.answer('Введите текст рассылки', reply_markup=back_admin_menu)
    await Mailing.text.set()


async def command_back_admin_menu1(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.answer('Данные которые вы ввели при создание рассылки не сохраняться', show_alert=True)
    await call.message.edit_text('Ваша панель управления', reply_markup=admin_menu)
    if await state.get_state() is not None:
        await state.finish()


def register_mailing(dp: Dispatcher):
    dp.register_callback_query_handler(create_mailing1, text='mailing', is_admin=True)
    dp.register_message_handler(create_mailing2, state=Mailing.text, is_admin=True)
    dp.register_callback_query_handler(create_mailing3, text='confirm_mailing', state=Mailing.confirm)
    dp.register_callback_query_handler(change_mailing, text='change_mailing', state=Mailing.confirm)
    dp.register_callback_query_handler(command_back_admin_menu1, text='mailing back admin menu', state=Mailing, is_admin=True)
