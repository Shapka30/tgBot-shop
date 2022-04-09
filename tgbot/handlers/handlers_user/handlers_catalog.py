from aiogram import Dispatcher
from aiogram import types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.config import db


async def empty_query(query: types.InlineQuery):
    user_id = query.from_user.id
    if await db.check_tg_user_id(user_id):
        if query.query == '':
            list_products = await db.select_all_products()
        else:
            list_products = await db.select_all_products_like(f'{query.query}%')

        show_products = [InlineQueryResultArticle(
            id=product[0],
            title=product[1],
            input_message_content=InputTextMessageContent(message_text=f'название: <b>{product[1]}</b>\n'
                                                                       f'Описание: <b>{product[3]}</b>\n'
                                                                       f'Цена: <b>{product[4]}</b> Руб.',
                                                          parse_mode='HTML'),
            description=f'{product[4]} Руб',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                text='Показать товар', url=f'https://t.me/Shapka30Tg_bot?start={product[0]}')]])
        ) for product in list_products]
        await query.answer(show_products)
    else:
        await query.answer(
            results=[],
            switch_pm_text='Бот не доступен. Подключить бота',
            switch_pm_parameter='connect_user'
        )


def register_inline_mode(dp: Dispatcher):
    dp.register_inline_handler(empty_query)
