from random import choice
from typing import Union


def create_invitation_code()->str:
    args = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    password = str()
    for _ in range(6):
        password += choice(args)
    return password


async def chek(user_id, channel: Union[str, int]):
    from aiogram import Bot
    bot = Bot.get_current()
    member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    return member.is_chat_member()