import ctypes
from typing import Union, List, Tuple, AnyStr, Optional
from zipfile import ZipFile, ZIP_DEFLATED


class MemoryStorage:
    """
    Creates a storage in the memory.
    """

    def __init__(self):
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
            output_file_path: str = "f.zip",
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
