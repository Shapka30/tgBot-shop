from aiogram import Dispatcher
from aiogram import types
from aiogram.utils.deep_linking import get_start_link
from tgbot.misc.variables import db
from tgbot.keyboards.inline import user_menu


async def referals(call: types.CallbackQuery):
    user_id = call.from_user.id
    count_referals = await db.select_count_referals(user_id)
    balance = await db.select_balance(user_id)
    invitation_code = await db.select_invitation_code(user_id)
    user_deeplink = await get_start_link(payload=user_id)

    await call.message.delete()
    await call.message.answer(f'Вы пригласили {count_referals}\n'
                              f'Количество ваших скидочных балов состовляет: {balance}\n'
                              'Балы будут вычитаться из стоймости покупки автоматически\n\n'
                              'ПРАВИЛА\n'
                              'Если у вас приглашеных пользователей до 10 человек, то вам будет начисляться 10 скидочных баллов\n'
                              'Если у вас приглашеных пользователей от 10 до 20 человек, то вам будет начисляться 15 скидочных баллов\n'
                              'Если у вас приглашеных пользователей более 20 человек, то вам будет начисляться 20 скидочных баллов\n\n'
                              f'Ваша ссылка для приглашения: {user_deeplink}\n'
                              f'Вашкод приглашения: {invitation_code}')

    await call.message.answer('Ваша панель управления', reply_markup=user_menu)


def register_referals(dp: Dispatcher):
    dp.register_callback_query_handler(referals, text='referals')
