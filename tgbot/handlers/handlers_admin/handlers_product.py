from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext

from tgbot.config import db
from tgbot.keyboards.inline import admin_menu, chek_product_menu, back_products_menu, admin_products_menu
from tgbot.misc.states import NewProduct


async def add_new_product1(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text('Введите название товара', reply_markup=back_products_menu)
    await NewProduct.name.set()


async def add_new_product2(message: types.Message, state: FSMContext):
    name = message.text
    if len(name) > 100:
        await message.answer('❌В название слишком много символов❌\n'
                             'Пришлите новое название'
                             'В название товара должно быть не боллее 100 символов\n'
                             'Символами является: буквы, цифры, всевозможные знаки припенания, смайлики и т.д', reply_markup=back_products_menu)
    else:
        await state.update_data(name=name)
        await message.answer('Пришлите фото товара(НЕ документ)', reply_markup=back_products_menu)
        await NewProduct.photo.set()


async def add_new_product3(message: types.Message, state: FSMContext):
    photo = str(message.photo[-1].file_id)
    await state.update_data(photo=photo)
    await message.answer('Пришлите описание товара', reply_markup=back_products_menu)
    await NewProduct.description.set()


async def add_new_product4(message: types.Message, state: FSMContext):
    text = message.text
    if len(text) > 650:
        await message.answer('❌В описание слишком много символов❌\n'
                             'Пришлите новое описание'
                             'В описание товара должно быть не боллее 650 символов\n'
                             'Символами является: буквы, цифры, всевозможные знаки припенания, смайлики и т.д', reply_markup=back_products_menu)
    else:
        await state.update_data(description=message.text)
        await message.answer('Пришлите цену товара(целое число)', reply_markup=back_products_menu)
        await NewProduct.price.set()


async def add_new_product5(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
        await state.update_data(price=price)
        await message.answer('Пришлите количество товара(целое число)', reply_markup=back_products_menu)
        await NewProduct.amount.set()
    except ValueError:
        await message.answer('❌Вы ввели неправильно значение❌\n'
                             'Пришлите еще раз цену товара(ЦЕЛОЕ ЧИСЛО)', reply_markup=back_products_menu)


async def add_new_product6(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
        await state.update_data(amount=amount)
        await message.answer('Введите артикул(целое число)', reply_markup=back_products_menu)
        await NewProduct.article.set()
    except ValueError:
        await message.answer('❌Вы ввели неправильно значение❌\n'
                             'Пришлите еще раз количество товара(ЦЕЛОЕ ЧИСЛО)', reply_markup=back_products_menu)


async def add_new_product7(message: types.Message, state: FSMContext):
    try:
        article = int(message.text)
        if await db.chek_article(article):
            await message.answer('Такой артикул уже есть. Ведите другой')
        else:
            await state.update_data(article=article)
            data = await state.get_data()
            await message.answer_photo(photo=data['photo'],
                                       caption='{0}\nОписание: {1}\nЦена: {2} рублей\nИмеется в наличии {3}\nАртику: {4}\nПодтверждаете ?'.format(
                                           data['name'], data['description'], data['price'], data['amount'],
                                           data['article']),
                                       reply_markup=chek_product_menu)
            await NewProduct.confirm.set()
    except ValueError:
        await message.answer('❌Вы ввели неправильно значение❌\n'
                             'Пришлите еще раз свой артикул(ЦЕЛОЕ ЧИСЛО)', reply_markup=back_products_menu)


async def add_new_product8(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    await db.add_products(**data)
    await call.message.answer('Товар успешно добавлен в базу данных')
    await call.message.answer('Ваша панель управления', reply_markup=admin_menu)
    if await state.get_state() is None:
        return
    await state.finish()


async def again_product(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    if await state.get_state() is None:
        return
    await state.finish()
    await NewProduct.name.set()
    await call.message.delete()
    await call.message.answer('Введите название товара', reply_markup=back_products_menu)


async def cencellation_product(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer('Ваша панель управления товарами', reply_markup=admin_products_menu)
    if await state.get_state() is not None:
        await state.finish()


async def command_back_menu_products1(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.answer('Данные которые вы ввели при добавление товара не сохраняться', show_alert=True)
    await call.message.delete()
    await call.message.answer('Ваша панель управления товарами', reply_markup=admin_products_menu)
    if await state.get_state() is not None:
        await state.finish()


def register_add_product(dp: Dispatcher):
    # регестрация хендлеров добавления товара

    dp.register_callback_query_handler(add_new_product1, text='add new product', is_admin=True)
    dp.register_message_handler(add_new_product2, state=NewProduct.name)
    dp.register_message_handler(add_new_product3, state=NewProduct.photo, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(add_new_product4, state=NewProduct.description)
    dp.register_message_handler(add_new_product5, state=NewProduct.price)
    dp.register_message_handler(add_new_product6, state=NewProduct.amount)
    dp.register_message_handler(add_new_product7, state=NewProduct.article)
    dp.register_callback_query_handler(add_new_product8, text='confirm', state=NewProduct.confirm, is_admin=True)
    dp.register_callback_query_handler(again_product, text='change', state=NewProduct.confirm, is_admin=True)

    # регистрация хендлера назад в меню
    dp.register_callback_query_handler(cencellation_product, text='chek back admin pr menu', state=NewProduct.confirm)
    dp.register_callback_query_handler(command_back_menu_products1, text='back_products_menu', state=NewProduct,
                                       is_admin=True)
