from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hcode

from tgbot.pop import db


async def select_pay_bill(call: CallbackQuery):
    user_id = call.from_user.id
    data = list()
    data1 = str()
    all_pay_bill = list(await db.select_all_bill_pay_for_user(user_id))

    if all_pay_bill:
        for bill in all_pay_bill:
            data1 += f'{str(bill[4])}\n'
            data1 += f'Сумма покупки: {str(bill[2])}\n'
            data1 += f'Скидка: {int(bill[3])} рублей\n'
            data1 += f'Колличество: {str(bill[0])}\n'
            data1 += f'Адресс доставки: {str(bill[1])}\n'
            data.append(data1)
            data1 = str()
        answer = '\n\n'.join(data)
        await call.message.answer('Все ваши оплаченые заказы:\n\n'
                                  f'{answer}')
    else:
        await call.message.answer('Вы пока ничего не купили')


def register_pay_bill(dp: Dispatcher):
    dp.register_callback_query_handler(select_pay_bill, text='catalog')
