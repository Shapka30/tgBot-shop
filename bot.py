import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.db_postgres.postgreSQL import Database
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.handlers_admin.handlers_product import register_add_product
from tgbot.handlers.handlers_admin.admin import register_admin
from tgbot.handlers.handlers_admin.mailing import register_mailing
from tgbot.handlers.handlers_admin.other_handlers_product import register_other_handlers_product
from tgbot.handlers.handlers_bd import register_all_handlers_db
from tgbot.handlers.handlers_buy import register_handlers_buy
from tgbot.handlers.handlers_user.handlers_catalog import register_inline_mode
from tgbot.handlers.handlers_user.handlers_pay_bill import register_pay_bill
from tgbot.handlers.handlers_user.handlers_referals import register_referals
from tgbot.handlers.handlers_user.user import register_user


from tgbot.middlewares.throttling import ThrottlingMiddleware
from tgbot.pop import db

logger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    dp.setup_middleware(ThrottlingMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_handlers_buy(dp)
    register_admin(dp)
    register_user(dp)
    register_add_product(dp)
    register_other_handlers_product(dp)
    register_mailing(dp)
    register_pay_bill(dp)
    register_inline_mode(dp)
    register_referals(dp)
    register_all_handlers_db(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)
    await db.create()
    await db.create_table_users()
    await db.create_table_products()
    await db.create_table_payment()

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")