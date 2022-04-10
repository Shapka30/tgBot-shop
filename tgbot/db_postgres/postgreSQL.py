from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from tgbot.config import load_config

config = load_config('.env')

class Database():

    def init(self):
        self.pool: Union[Pool, None]

    async def create(self):
        self.pool = await asyncpg.create_pool(
            host=config.db.host,
            password=config.db.password,
            user=config.db.user,
            database=config.db.database
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:  # достать все
                    result = await connection.fetch(command, *args)
                elif fetchval:  # достать одно значение
                    result = await connection.fetchval(command, *args)
                elif fetchrow:  # достать одну строку
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += ' AND '.join([
            f'{item} = ${num}' for num, item in enumerate(parameters.keys(), start=1)
        ])
        return sql, tuple(parameters.values())

    # часть с таблицой users

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users(
            user_id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            username VARCHAR(255) NULL,
            telegram_user_id BIGINT NOT NULL UNIQUE,
            referal INT NULL,
            invitation_code VARCHAR(8) NOT NULL UNIQUE,
            balance INT DEFAULT 0,
            count_referals INT DEFAULT 0
        );
        """
        await self.execute(sql, execute=True)

    async def add_user(self, first_name: str, username: str, telegram_user_id: int, invitation_code: str,
                       referal: int = None):
        sql = """INSERT INTO users (first_name, username, telegram_user_id, invitation_code, referal) VALUES($1, $2, $3, $4, $5)"""
        return await self.execute(sql, first_name, username, telegram_user_id, invitation_code, referal, execute=True)

    async def increase_balance(self, balls, telegram_user_id):
        sql = """UPDATE users SET balance = balance + $1 WHERE telegram_user_id = $2"""
        await self.execute(sql, balls, telegram_user_id, execute=True)

    async def update_balance(self, balance, telegram_user_id):
        sql = """UPDATE users SET balance = $1 WHERE telegram_user_id = $2"""
        await self.execute(sql, balance, telegram_user_id, execute=True)

    async def select_user(self, **kwargs):
        sql = """SELECT * FROM users WHERE """
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = """SELECT COUNT(*) FROM users"""
        return await self.execute(sql, fetchval=True)

    async def check_tg_user_id(self, telegram_user_id):
        sql = """SELECT True FROM users WHERE telegram_user_id = $1"""
        return await self.execute(sql, telegram_user_id, fetchrow=True)

    async def check_invitation_code(self, invitation_code):
        sql = """SELECT True FROM users WHERE invitation_code = $1"""
        return await self.execute(sql, invitation_code, fetchrow=True)

    async def select_tg_user_id(self, invitation_code):
        sql = """SELECT telegram_user_id FROM users WHERE invitation_code = $1"""
        return await self.execute(sql, invitation_code, fetchval=True)

    async def add_count_referals(self, telegram_user_id: int):
        sql = """UPDATE users SET count_referals = count_referals + 1 WHERE telegram_user_id = $1"""
        await self.execute(sql, telegram_user_id, execute=True)

    async def select_count_referals(self, telegram_user_id: int):
        sql = """SELECT count_referals FROM users WHERE telegram_user_id = $1"""
        return await self.execute(sql, telegram_user_id, fetchval=True)

    async def select_balance(self, telegram_user_id):
        sql = """SELECT balance FROM users WHERE telegram_user_id = $1"""
        return await self.execute(sql, telegram_user_id, fetchval=True)

    async def select_invitation_code(self, telegram_user_id: int):
        sql = """SELECT invitation_code FROM users WHERE telegram_user_id = $1"""
        return await self.execute(sql, telegram_user_id, fetchval=True)

    async def select_all_tg_users_id(self):
        sql = """SELECT telegram_user_id FROM users"""
        return await self.execute(sql, fetch=True)

    # часть с таблицой products

    async def create_table_products(self):
        sql = """
        CREATE TABLE IF NOT EXISTS products(
            product_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            photo VARCHAR(255) NOT NULL,
            description VARCHAR(650) NOT NULL,
            price INT NOT NULL,
            amount INT NOT NULL,
            article INT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def add_products(self, name: str, photo: str, description: str, price: int, amount: int, article: int):
        sql = """INSERT INTO products(name, photo, description, price, amount, article) VALUES($1, $2, $3, $4, $5, $6)"""
        await self.execute(sql, name, photo, description, price, amount, article, execute=True)

    async def chek_article(self, article: int):
        sql = """SELECT True FROM products WHERE article = $1"""
        return await self.execute(sql, article, fetchval=True)

    async def select_all_products(self):
        sql = """SELECT * FROM products ORDER BY name"""
        return await self.execute(sql, fetch=True)

    async def select_all_products_like(self, text):
        sql = """SELECT * FROM products WHERE name ILIKE $1 OR description ILIKE $1"""
        return await self.execute(sql, text, fetch=True)

    async def update_product_price(self, article: int, new_price: int):
        sql = """UPDATE products SET price = $2 WHERE article = $1"""
        await self.execute(sql, article, new_price, execute=True)

    async def update_product_amount(self, article: int, new_amount: int):
        sql = """UPDATE products SET amount = $2 WHERE article = $1"""
        await self.execute(sql, article, new_amount, execute=True)

    async def update_product_amount_id(self, product_id: int, new_amount: int):
        sql = """UPDATE products SET amount = $2 WHERE product_id = $1"""
        await self.execute(sql, product_id, new_amount, execute=True)

    async def select_product(self, product_id):
        sql = """SELECT * FROM products WHERE product_id = $1"""
        return await self.execute(sql, product_id, fetchrow=True)

    async def select_price(self, article: int):
        sql = """SELECT price FROM products WHERE article = $1"""
        return await self.execute(sql, article, fetchval=True)

    async def select_price_id(self, product_id: int):
        sql = """SELECT price FROM products WHERE product_id = $1"""
        return await self.execute(sql, product_id, fetchval=True)

    async def select_amount(self, article: int):
        sql = """SELECT amount FROM products WHERE article = $1"""
        return await self.execute(sql, article, fetchval=True)

    async def select_amount_id(self, product_id: int):
        sql = """SELECT amount FROM products WHERE product_id = $1"""
        return await self.execute(sql, product_id, fetchval=True)

    async def select_name_product(self, product_id: int):
        sql = """SELECT name FROM products WHERE product_id = $1"""
        return await self.execute(sql, product_id, fetchval=True)

    async def delete_product(self, article: int):
        sql = """DELETE FROM products WHERE article = $1"""
        await self.execute(sql, article, execute=True)

    # часть с таблицой payment

    async def create_table_payment(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS payment(
        pay_id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL,
        product_id INT NOT NULL,
        amount INT,
        delivery VARCHAR(100) NOT NULL,
        pay_status INT,
        bill_id VARCHAR(255) UNIQUE,
        price INT,
        discount INT DEFAULT 0
        );
        '''
        await self.execute(sql, execute=True)

    async def add_payment(self, telegram_id: int, product_id: int, amount: int, delivery: str, pay_status: int,
                          bill_id: int):
        sql = """
        INSERT INTO payment (telegram_id, product_id, amount, delivery, pay_status, bill_id)
        VALUES($1, $2, $3, $4, $5, $6);
        """
        await self.execute(sql, telegram_id, product_id, amount, delivery, pay_status, bill_id, execute=True)

    async def add_payment2(self, price: int, discount: int, product_id: int):
        sql = """
        UPDATE payment 
        SET price = $1, discount = $2
        WHERE product_id = $3
        """
        await self.execute(sql, price, discount, product_id, execute=True)

    async def check_bill_id(self, bill_id: int):
        sql = """SELECT True FROM payment WHERE bill_id = $1"""
        return await self.execute(sql, bill_id, fetchval=True)

    async def delete_payment(self, bill_id: int):
        sql = """DELETE FROM payment WHERE bill_id = $1"""
        await self.execute(sql, bill_id, fetchval=True)

    async def update_pay_status(self, bill_id, new_status):
        sql = """UPDATE payment SET pay_status = $2 WHERE bill_id = $1"""
        await self.execute(sql, bill_id, new_status, execute=True)

    async def select_all_bill_pay_for_user(self, telegram_id):
        sql = """
        SELECT payment.amount, delivery, payment.price, discount, name 
        FROM payment JOIN products ON payment.product_id = products.product_id
        WHERE pay_status = 1 AND telegram_id = $1
        """
        return await self.execute(sql, telegram_id, fetch=True)
