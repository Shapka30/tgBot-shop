from pyqiwip2p import QiwiP2P

from tgbot.config import load_config

config = load_config(".env")
p2p = QiwiP2P(auth_key=config.qiwi.secret_token)

