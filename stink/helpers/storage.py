from io import BytesIO
from os import path, walk
from zipfile import ZipFile, ZIP_DEFLATED
from typing import Union, List, Tuple, AnyStr, Optional
from getpass import getuser
from random import random
import ctypes


class MemoryStorage:
    """
    Creates a storage in the memory.
    """

    def __init__(self):
        self.__buffer = BytesIO()
        self.__files = []

    def add_from_memory(self, source_path: str, content: Union[str, bytes]) -> None:
        """
        Adds a file to the list of files.

        Parameters:
        - source_path [str]: File name or path inside the archive.
        - content [str|bytes]: File content.

        Returns:
        - None.
        """
        self.__files.append((source_path, content))

    def add_from_disk(self, source_path: str, zip_path: Optional[str] = None) -> None:
        """
        Adds a file path to the list of files.

        Parameters:
        - source_path [str]: File name or path to be copied.
        - zip_path [str]: Path to the file or folder in the archive.

        Returns:
        - None.
        """
        if path.isfile(source_path):
            if zip_path:
                self.__files.append((zip_path, open(source_path, "rb").read()))
            else:
                self.__files.append(
                    (path.basename(source_path), open(source_path, "rb").read())
                )

        elif path.isdir(source_path):
            for folder_name, _, file_names in walk(source_path):
                for file_name in file_names:
                    try:
                        file_path = path.join(folder_name, file_name)
                        name_in_zip = path.relpath(file_path, source_path)

                        if zip_path:
                            name_in_zip = path.join(zip_path, name_in_zip)

                        self.__files.append((name_in_zip, open(file_path, "rb").read()))
                    except Exception as e:
                        print(
                            f"[Storage]: Error while copying a file {file_name} - {repr(e)}"
                        )
        else:
            print("[Storage]: The file is unsupported.")

    def get_data(self) -> List:
        """
        Returns the contents of the archive.

        Parameters:
        - None.

        Returns:
        - None.
        """
        return self.__files

    def create_zip(
            self,
            files: Optional[List[Tuple[str, AnyStr]]] = None,
            output_file_path: str = f"{getuser()}.{random()}.zip",
    ):
        """
        Adds files from a list of data returned by get_data method of other MemoryStorage objects into one archive.

        Parameters:
        - files [list]: List of files for creating the archive.
        - output_file_path [str]: Path to the output ZIP file.

        Returns:
        None
        """
        if files is None:
            files = self.__files

        with ZipFile(output_file_path, mode="w", compression=ZIP_DEFLATED) as zip_file:
            for file_name, content in files:
                zip_file.writestr(file_name, content)
        ctypes.windll.kernel32.SetFileAttributesW(output_file_path, 0x02)
