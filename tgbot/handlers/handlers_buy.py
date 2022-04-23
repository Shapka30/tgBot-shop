import re

# import env as env
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyqiwip2p import QiwiP2P

from tgbot.misc.variables import config
from tgbot.misc.variables import db
from tgbot.keyboards.inline import buy_menu, user_menu, start_menu
from tgbot.misc.states import Buy

p2p = QiwiP2P(auth_key=config.qiwi.close_token)


async def start_buy(message: types.Message, state: FSMContext):
    if await db.check_tg_user_id(int(message.from_user.id)):

        if await state.get_state() is not None:
            await state.finish()
        product_id = int(message.get_args())
        await state.update_data(product_id=product_id)

        product = await db.select_product(product_id)
        photo = product[2]
        description = product[3]
        price = product[4]
        amount = product[5]
        await message.answer_photo(photo=photo, caption=f'Описание: {description}\n'
                                                        f'Цена: {price}\n'
                                                        f'Количество в наличии: {amount}', reply_markup=buy_menu)
    else:
        await message.answer('\n'.join([
            '❌Ошибка❌',
            '🔒У вас нет доступа!!!🔒',
            'Чтобы использывать бота введите код приглашения, либо пройдите по реферальной ссылке\n',
            'Если вас никто не пригласил, то подпишитесь на канал, что бы получить доступ к боту\n',
            'Ссылка на канал: https://t.me/test_bot_shop'
        ]), reply_markup=start_menu)


async def buy_product1(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    product_id = data['product_id']
    amount = await db.select_amount_id(product_id)
    await call.message.answer('Введите количество товара(целое число)\n'
                              f'Сейчас есть в наличии: {amount}')
    await Buy.amount.set()


async def buy_product2(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
        data = await state.get_data()
        product_id = data['product_id']
        all_amount = await db.select_amount_id(product_id)
        if amount > all_amount or amount < 0:
            await message.answer('❌В наличие нет столько товара❌\n'
                                 f'Сейчас есть в наличии: {all_amount}')
        else:
            await state.update_data(amount=amount)
            await message.answer('Введите адрес доставки(город, улица, дом)')
            await Buy.delivery.set()
    except ValueError:
        await message.answer('❌Вы ввели неправильно значение❌\n'
                             'Пришлите еще раз количество товара(ЦЕЛОЕ ЧИСЛО)')


async def buy_product3(message: types.Message, state: FSMContext):
    await state.update_data(delivery=message.text)

    data = await state.get_data()
    product_id = data['product_id']
    user_id = message.from_user.id
    delivery = data['delivery']
    balance = await db.select_balance(user_id)
    price = await db.select_price_id(product_id)
    amount = data['amount']

    if amount * price - balance < 1:
        balance -= amount * price - 1
        discount = amount * price - 1
        sum = 1
    else:
        discount = balance
        sum = amount * price - balance
        balance = 0

    await state.update_data(balance=balance, discount=discount, sum=sum)

    name_product = await db.select_name_product(product_id)
    comment = f'Товар: {name_product}(количество: {amount})'
    bill = p2p.bill(amount=sum, lifetime=15, comment=comment)

    bill_id = str(bill.bill_id)
    await db.add_payment(user_id, product_id, amount, delivery, 0, bill_id)

    await message.answer('Скидка за приглашенных пользователей применится автоматически\n'
                         'После оплаты обязательно нажмити кнопку "Проверить оплату"\n'
                         f'К оплате {sum} рублей', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💰Оплатить💰', url=bill.pay_url)],
        [InlineKeyboardButton(text='Проверить оплату', callback_data=f'check_{bill_id}')]
    ]))
    await Buy.confirm.set()


async def check_bill(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    bill_id = call.data[6:]
    if await db.check_bill_id(bill_id):
        if str(p2p.check(bill_id=bill_id).status) == 'PAID':
            await call.message.edit_text('Товар успешно оплачен\n'
                                         'Если у вас будут какие то вопросы то обращайтесь (какие то контакты)')
            await call.message.answer('Ваша панель управления', reply_markup=user_menu)

            data = await state.get_data()
            balance = data['balance']
            product_id = data['product_id']
            amount = data['amount']
            price = data['sum']
            discount = data['discount']
            user_id = call.from_user.id

            new_amount = await db.select_amount_id(product_id) - amount

            await db.add_payment2(price, discount, product_id)
            await db.update_product_amount_id(product_id, new_amount)
            await db.update_balance(balance, user_id)
            await db.update_pay_status(bill_id, 1)
            if await state.get_state() is not None:
                await state.finish()
        else:
            await call.message.answer('Вы еще не оплатили заказ')
            if await state.get_state() is not None:
                await state.finish()
    else:
        await call.message.answer('Такого заказа не найдено')
        if await state.get_state() is not None:
            await state.finish()


async def back_user_menu_pay(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer('Ваша панель управления', reply_markup=user_menu)
    if await state.get_state() is not None:
        await state.finish()


def register_handlers_buy(dp: Dispatcher):
    dp.register_callback_query_handler(buy_product1, text='buy')
    dp.register_message_handler(buy_product2, state=Buy.amount)
    dp.register_message_handler(buy_product3, state=Buy.delivery)
    dp.register_callback_query_handler(check_bill, text_contains='check_', state=Buy.confirm)
    dp.register_callback_query_handler(back_user_menu_pay, text='buy_back', state=Buy)

    dp.register_message_handler(start_buy, CommandStart(deep_link=re.compile(r"^[0-9]{1,3}$")))
