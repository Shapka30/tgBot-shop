import re

import asyncpg.exceptions
from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.deep_linking import get_start_link

from tgbot.config import db
from tgbot.keyboards.inline import start_menu, start_menu2, back_start_menu, user_menu
from tgbot.misc.help_function import create_invitation_code, chek
from tgbot.misc.throttling import rate_limit


@rate_limit(5)
async def user_start_deeplink(message: types.Message):
    arg = int(message.get_args())
    if await db.check_tg_user_id(arg):
        try:

            user_invition_code = create_invitation_code()
            while await db.check_invitation_code(user_invition_code):
                user_invition_code = create_invitation_code()

            await db.add_user(
                first_name=message.from_user.full_name,
                username=message.from_user.username,
                telegram_user_id=message.from_user.id,
                invitation_code=user_invition_code,
                referal=arg
            )

            user_deeplink = await get_start_link(payload=message.from_user.id)

            count_referals = await db.select_count_referals(arg)
            if count_referals <= 10:
                await db.increase_balance(10, arg)
            elif 10 < count_referals < 20:
                await db.increase_balance(15, arg)
            else:
                await db.increase_balance(20, arg)

            await db.add_count_referals(arg)

            await message.answer('\n'.join([
                f'🎉Поздравляю {message.from_user.first_name}, вы получили доступ🎉',
                'Вы можете получить 10 бонусных балов за каждого преглашонного вами пользователя!!!',
                f'Ваша реферальная ссылка: {user_deeplink}',
                f'Ваш код приглашения: {user_invition_code}'
            ]))

        except asyncpg.exceptions.UniqueViolationError:
            await message.answer('Ваша панель управления', reply_markup=user_menu)
    else:
        await message.answer('У вас не правильная реферальная ссылка')

@rate_limit(5)
async def user_start(message: types.Message, state: FSMContext):
    if await state.get_state() is not None:
        await state.finish()
    user_id = int(message.from_user.id)
    if await db.check_tg_user_id(user_id):
        await message.answer('Ваша панель управления', reply_markup=user_menu)
    else:
        await message.answer('\n'.join([
            '❌Ошибка❌',
            '🔒У вас нет доступа!!!🔒',
            'Чтобы использывать бота введите код приглашения, либо пройдите по реферальной ссылке\n',
            'Если вас никто не пригласил, то подпишитесь на канал, что бы получить доступ к боту\n',
            'Ссылка на канал: https://t.me/test_bot_shop'
        ]), reply_markup=start_menu)


async def chek_invitation_code(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text='Пришлите код приглашения', reply_markup=back_start_menu)
    # await Invitation_code.state1.set()
    await state.set_state('start1')


async def chek_invitation_code2(message: types.Message, state: FSMContext):
    text = message.text
    if await db.check_invitation_code(text):

        user_invition_code = create_invitation_code()
        while await db.check_invitation_code(user_invition_code):
            user_invition_code = create_invitation_code()

        arg = await db.select_tg_user_id(text)

        await db.add_user(
            first_name=message.from_user.full_name,
            username=message.from_user.username,
            telegram_user_id=message.from_user.id,
            invitation_code=user_invition_code,
            referal=arg
        )

        count_referals = await db.select_count_referals(arg)
        if count_referals <= 10:
            await db.increase_balance(10, arg)
        elif 10 < count_referals < 20:
            await db.increase_balance(15, arg)
        else:
            await db.increase_balance(20, arg)

        await db.add_count_referals(arg)
        user_deeplink = await get_start_link(payload=message.from_user.id)

        await message.answer('\n'.join([
            f'🎉Поздравляю {message.from_user.first_name}, вы получили доступ🎉',
            'Вы можете получить 10 бонусных балов за каждого преглашонного вами пользователя!!!',
            f'Ваша реферальная ссылка: {user_deeplink}',
            f'Ваш код приглашения: {user_invition_code}'
        ]))
        await message.answer('Ваша панель управления', reply_markup=user_menu)

        if await state.get_state() is None:
            return
        await state.finish()
    else:
        await message.answer('❌Вы вели неправильный код приглошения❌', reply_markup=start_menu2)
        await state.finish()


async def check_subscription(call: types.CallbackQuery, state: FSMContext):
    if await state.get_state() is not None:
        await state.finish()

    user_id = call.from_user.id

    user_invition_code = create_invitation_code()
    while await db.check_invitation_code(user_invition_code):
        user_invition_code = create_invitation_code()

    user_deeplink = await get_start_link(payload=user_id)

    if await chek(user_id=user_id, channel='-1001707518912'):
        await db.add_user(
            first_name=call.from_user.full_name,
            username=call.from_user.username,
            telegram_user_id=user_id,
            invitation_code=user_invition_code
        )
        await call.message.answer('\n'.join([
            f'🎉Поздравляю {call.from_user.first_name}, вы получили доступ🎉',
            'Вы можете получить 10 бонусных балов за каждого преглашонного вами пользователя!!!',
            f'Ваша реферальная ссылка: {user_deeplink}',
            f'Ваш код приглашения: {user_invition_code}'
        ]))
        await call.message.answer('Ваша панель управления', reply_markup=user_menu)

    else:
        await call.message.answer('\n'.join([
            '❌Ошибка❌',
            '🔒У вас нет доступа!!!🔒',
            'Чтобы использывать бота введите код приглашения, либо пройдите по реферальной ссылке\n',
            'Если вас никто не пригласил, то подпишитесь на канал, что бы получить доступ к боту\n',
            'Ссылка на канал: https://t.me/test_bot_shop'
        ]), reply_markup=start_menu)


async def comeback_start_menu(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text('\n'.join([
        '❌Ошибка❌',
        '🔒У вас нет доступа!!!🔒',
        'Чтобы использывать бота введите код приглашения, либо пройдите по реферальной ссылке\n',
        'Если вас никто не пригласил, то подпишитесь на канал, что бы получить доступ к боту\n',
        'Ссылка на канал: https://t.me/test_bot_shop'
    ]), reply_markup=start_menu)
    if await state.get_state() is None:
        return
    await state.finish()




def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start_deeplink, CommandStart(deep_link=re.compile(r"^[0-9]{4,10}$")))
    dp.register_message_handler(user_start, CommandStart())
    dp.register_callback_query_handler(chek_invitation_code, text='code')
    dp.register_message_handler(chek_invitation_code2, state='start1')
    dp.register_callback_query_handler(check_subscription, text='check subscription')
    dp.register_callback_query_handler(comeback_start_menu, text='start menu back', state='start1')
