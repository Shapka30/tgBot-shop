from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.pop import db
from tgbot.keyboards.inline import admin_menu, chek_update_price_menu, back_products_menu, admin_products_menu, \
    delete_product, chek_update_amount_menu
from tgbot.misc.states import ChangePrice, DeleteProduct, ChangeAmount


# CHANGE PRICE


async def change_product_price1(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text(text='Введите артикул товара у которого хотите поменять цену',
                                 reply_markup=back_products_menu)
    await ChangePrice.article.set()


async def change_product_price2(message: types.Message, state: FSMContext):
    try:
        article = int(message.text)
        if await db.chek_article(article):
            await state.update_data(article=article)
            old_price = await db.select_price(article)
            await message.answer('Введите новую цену(целое число)\n'
                                 f'Старая цена: {old_price}', reply_markup=back_products_menu)
            await ChangePrice.price.set()
        else:
            await message.answer('❌Ошибка❌\n'
                                 'Такого артикула не существует', reply_markup=back_products_menu)
    except ValueError:
        await message.answer('❌Вы ввели неправильно значение❌\n'
                             'Пришлите еще раз свой артикул(ЦЕЛОЕ ЧИСЛО)', reply_markup=back_products_menu)


async def change_product_price3(message: types.Message, state: FSMContext):
    try:
        new_price = int(message.text)
        await state.update_data(new_price=new_price)
        data = await state.get_data()
        await message.answer('Артикул: {0}\n'
                             'Новая цена: {1}'.format(data['article'], data['new_price']),
                             reply_markup=chek_update_price_menu)
        await ChangePrice.confirm.set()
    except ValueError:
        await message.answer('❌Вы ввели неправильно значение❌\n'
                             'Пришлите еще раз новую цену товара(ЦЕЛОЕ ЧИСЛО)', reply_markup=back_products_menu)


async def update_price(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    await db.update_product_price(**data)
    if await state.get_state() is not None:
        await state.finish()
    await call.message.answer('Цена успешно обновлена')
    await call.message.answer('Ваша панель управления', reply_markup=admin_menu)


async def change_price(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    if await state.get_state() is not None:
        await state.finish()
    await call.message.edit_text('Введите артикул товара у которого хотите поменять цену',
                                 reply_markup=back_products_menu)
    await ChangePrice.article.set()


async def no_change_price(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    if await state.get_state() is not None:
        await state.finish()
    await call.message.edit_text('Ваша панель управления товарами', reply_markup=admin_products_menu)


# DELETE PRODUCT


async def delete_product1(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer('Введите артикул товара который хотите удалить', reply_markup=back_products_menu)
    await DeleteProduct.article.set()


async def delete_product2(message: types.Message, state: FSMContext):
    try:
        article = int(message.text)
        if await db.chek_article(article):
            await state.update_data(article=article)
            await message.answer(f'ВЫ УВЕРЕНЫ ЧТО ХОТИТЕ УДАЛИТЬ ТОВАР С АРТИКЛЕМ {article}',
                                 reply_markup=delete_product)
            await DeleteProduct.confirm.set()
        else:
            await message.answer('❌Ошибка❌\n'
                                 'Такого артикула не существует', reply_markup=back_products_menu)
    except ValueError:
        await message.answer('❌Вы ввели неправильно значение❌\n'
                             'Пришлите еще раз свой артикул(ЦЕЛОЕ ЧИСЛО)', reply_markup=back_products_menu)


async def delete_product_yes(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    await db.delete_product(**data)
    await call.message.answer('Товар был успешно удален')
    await call.message.answer('Ваша панель управления', reply_markup=admin_menu)
    if await state.get_state() is not None:
        await state.finish()


async def delete_product_no(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    if await state.get_state() is not None:
        await state.finish()
    await call.message.edit_text('Ваша панель управления товарами', reply_markup=admin_products_menu)


async def command_back_menu_products2(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.answer('Данные которые вы ввели не сохраняться', show_alert=True)
    await call.message.edit_text('Ваша панель управления товарами', reply_markup=admin_products_menu)
    if await state.get_state() is not None:
        await state.finish()


# CHANGE AMOUNT


async def change_amount1(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer('Введите артикул товара у которого хотите поменять количество',
                              reply_markup=back_products_menu)
    await ChangeAmount.article.set()


async def change_amount2(message: types.Message, state: FSMContext):
    try:
        article = int(message.text)
        amount = await db.select_amount(article)
        if await db.chek_article(article):
            await state.update_data(article=article)
            await message.answer(f'Введите новое количество товара\n'
                                 f'Текущее количество: {amount}', reply_markup=back_products_menu)
            await ChangeAmount.amount.set()
        else:
            await message.answer('❌Ошибка❌\n'
                                 'Такого артикула не существует', reply_markup=back_products_menu)
    except ValueError:
        await message.answer('❌Вы ввели неправильно значение❌\n'
                             'Пришлите еще раз свой артикул(ЦЕЛОЕ ЧИСЛО)', reply_markup=back_products_menu)


async def change_amount3(message: types.Message, state: FSMContext):
    try:
        new_amount = int(message.text)
        await state.update_data(new_amount=new_amount)
        data = await state.get_data()
        await message.answer('Артикул: {0}\n'
                             'Новое количество: {1}'.format(data['article'], data['new_amount']),
                             reply_markup=chek_update_amount_menu)
        await ChangeAmount.confirm.set()
    except ValueError:
        await message.answer('❌Вы ввели неправильно значение❌\n'
                             'Пришлите еще раз количество товара(ЦЕЛОЕ ЧИСЛО)', reply_markup=back_products_menu)


async def change_amount4(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    await db.update_product_amount(**data)
    await call.message.answer('Количество успешно изменено')
    await call.message.answer('Ваша панель управления товарами', reply_markup=admin_products_menu)
    if await state.get_state() is not None:
        await state.finish()


async def change_change_amount(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    if await state.get_state() is not None:
        await state.finish()
    await call.message.answer('Введите артикул товара у которого хотите поменять количество',
                              reply_markup=back_products_menu)
    await ChangeAmount.article.set()


async def no_change_amount(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    if await state.get_state() is not None:
        await state.finish()
    await call.message.edit_text('Ваша панель управления товарами', reply_markup=admin_products_menu)


# REGISTER


def register_other_handlers_product(dp: Dispatcher):
    # update price

    dp.register_callback_query_handler(change_product_price1, text='change_price', is_admin=True)
    dp.register_message_handler(change_product_price2, state=ChangePrice.article)
    dp.register_message_handler(change_product_price3, state=ChangePrice.price)
    dp.register_callback_query_handler(update_price, text='confirm_new_price', state=ChangePrice.confirm, is_admin=True)
    dp.register_callback_query_handler(change_price, text='change_new_price', state=ChangePrice.confirm, is_admin=True)
    dp.register_callback_query_handler(no_change_price, text='new price back admin menu', state=ChangePrice.confirm,
                                       is_admin=True)

    # delete

    dp.register_callback_query_handler(delete_product1, text='delete product', is_admin=True)
    dp.register_message_handler(delete_product2, state=DeleteProduct.article)
    dp.register_callback_query_handler(delete_product_yes, text='delete_yes', state=DeleteProduct.confirm)
    dp.register_callback_query_handler(delete_product_no, text='delete_no', state=DeleteProduct.confirm)

    # update amount

    dp.register_callback_query_handler(change_amount1, text='change_amount', is_admin=True)
    dp.register_message_handler(change_amount2, state=ChangeAmount.article)
    dp.register_message_handler(change_amount3, state=ChangeAmount.amount)
    dp.register_callback_query_handler(change_amount4, text='confirm_new_amount', state=ChangeAmount.confirm,
                                       is_admin=True)
    dp.register_callback_query_handler(change_change_amount, text='change_new_amount', state=ChangeAmount.confirm,
                                       is_admin=True)
    dp.register_callback_query_handler(no_change_amount, text='new amount back admin menu', state=ChangeAmount.confirm,
                                       is_admin=True)

    # back products menu

    dp.register_callback_query_handler(command_back_menu_products2, text='back_products_menu',
                                       state=[ChangePrice, ChangeAmount, DeleteProduct],
                                       is_admin=True)
