from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# inline для пользователей


start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✏️Код пригралашения✏️', callback_data='code')],
    [InlineKeyboardButton(text='🔎 Проверить подписку на канал 🔎',
                          callback_data='check subscription')]
])

start_menu2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='start menu back')],
    [InlineKeyboardButton(text='Попробовать еще раз', callback_data='code')]
])

back_start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Назад', callback_data='start menu back')
    ]
])

user_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🛒Каталог', switch_inline_query_current_chat='')],
    [InlineKeyboardButton(text='🌐Рефералы', callback_data='referals')],
    [InlineKeyboardButton(text='💰Оплачениые заказы💰', callback_data='catalog')]
])

# inline для админов


admin_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Показать количество пользователей',
                          callback_data='count users')],
    [InlineKeyboardButton(text='Товары',
                          callback_data='products')],
    [InlineKeyboardButton(text='Создать рассылку', callback_data='mailing')]
])

admin_products_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить товар', callback_data='add new product')],
    [InlineKeyboardButton(text='Удалить товар', callback_data='delete product')],
    [InlineKeyboardButton(text='Поменять цену товара', callback_data='change_price')],
    [InlineKeyboardButton(text='Поменять количество товара', callback_data='change_amount')],
    [InlineKeyboardButton(text='Вернуться в панель управления', callback_data='back admin menu')]
])

chek_product_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='confirm')],
    [InlineKeyboardButton(text='Вести заново', callback_data='change')],
    [InlineKeyboardButton(text='Отменить', callback_data='chek back admin pr menu')]
])

back_admin_menu = InlineKeyboardMarkup(row_width=1,
                                       inline_keyboard=[
                                           [InlineKeyboardButton(text='Вернуться в панель управления',
                                                                 callback_data='back admin menu')]
                                       ])

back_products_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться в меню управления товарами', callback_data='back_products_menu')]
])

chek_mailing_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтверждаю', callback_data='confirm_mailing')],
    [InlineKeyboardButton(text='Заполнить заново', callback_data='change_mailing')],
    [InlineKeyboardButton(text='Отменить', callback_data='mailing back admin menu')]
])

chek_update_price_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтверждаю', callback_data='confirm_new_price')],
    [InlineKeyboardButton(text='Заполнить заново', callback_data='change_new_price')],
    [InlineKeyboardButton(text='Отменить', callback_data='new price back admin menu')]
])

chek_update_amount_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтверждаю', callback_data='confirm_new_amount')],
    [InlineKeyboardButton(text='Заполнить заново', callback_data='change_new_amount')],
    [InlineKeyboardButton(text='Отменить', callback_data='new amount back admin menu')]
])

delete_product = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='delete_yes')],
    [InlineKeyboardButton(text='Нет', callback_data='delete_no')]
])

# OTHER

buy_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💎Купить', callback_data='buy')],
    [InlineKeyboardButton(text='Назад', switch_inline_query_current_chat='', callback_data='buy_back')]
])
