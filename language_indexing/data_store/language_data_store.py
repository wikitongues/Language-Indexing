from abc import ABC, abstractmethod
from typing import List, Optional

from ..language import Language
from .response_object import ResponseObject


class LanguageDataStore(ABC):
    """
    Interface for language data store

    Args:
        ABC
    """

    @abstractmethod
    def get_language(self, iso_code: str) -> ResponseObject[Language]:
        """
        Retrieve a language from the data store by the given ISO code

        Args:
            iso_code (str): ISO code
        """
        pass

    @abstractmethod
    def get_languages(self, iso_codes: List[str]) -> ResponseObject[List[Language]]:
        """
        Retrieve multiple languages from the data store by ISO code

        Args:
            iso_codes (list): List of ISO codes
        """
        pass

    @abstractmethod
    def list_languages(
        self, page_size: Optional[int], offset: Optional[str], max_records: Optional[int]
    ) -> ResponseObject[List[Language]]:
        """
        List languages from the data store

        Args:
            page_size (int): Page size
            offset (str): Offset value for pagination
            max_records (int): Max records to retrieve
        """
        pass
