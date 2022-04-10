from tgbot.db_postgres.postgreSQL import Database

from tgbot.config import load_config

config = load_config(".env")

db = Database()
