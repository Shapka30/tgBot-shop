from dataclasses import dataclass

from environs import Env


@dataclass
class Payment:
    token: str
    wallet: str
    open_token: str
    close_token: str


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous
    qiwi: Payment


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous(),
        qiwi=Payment(
            token=env.str('QIWI_TOKEN'),
            open_token=env.str('QIWI_OPEN_TOKEN'),
            close_token=env.str('QIWI_CLOSE_TOKEN'),
            wallet=env.str('QIWI_WALLET')
        )
    )



