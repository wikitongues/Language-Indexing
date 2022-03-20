from abc import ABC, abstractmethod
from typing import Iterable, Set

from .data_store.language_data_store import LanguageDataStore
from .lang_to_iso_converter import ILangToIsoConverter


class IResourceLanguageService(ABC):
    """
    Resource language service interface

    Args:
        ABC
    """

    @abstractmethod
    def get_resource_language_ids(self, lang_attrs):
        pass


class ResourceLanguageService(IResourceLanguageService):
    """
    Gets Airtable ID's for languages corresponding to lang attribute values

    Args:
        IResourceLanguageService
    """

    def __init__(self, language_data_store: LanguageDataStore, lang_to_iso_converter: ILangToIsoConverter) -> None:
        """
        Construct ResourceLanguageService

        Args:
            language_data_store (ILanguageDataStore): language data store
            lang_to_iso_converter (ILangToIsoConverter): lang to iso converter
        """

        self._language_data_store = language_data_store
        self._lang_to_iso_converter = lang_to_iso_converter
        self._cache = {}

    def get_resource_language_ids(self, lang_attrs: Iterable[str]) -> Set[str]:
        """
        Gets Airtable ID's for languages corresponding to lang attribute values

        Args:
            lang_attrs (iterable): lang attribute values

        Returns:
            set: Airtable ID's
        """

        resource_language_ids = set()

        for lang_attr in lang_attrs:
            iso = self._lang_to_iso_converter.get_iso_code(lang_attr)

            if not isinstance(iso, str):
                continue

            if iso not in self._cache:
                result = self._language_data_store.get_language(iso)

                if result.has_error():
                    continue

                resource_language = result.data

                if resource_language is None:
                    self._cache[iso] = None
                else:
                    self._cache[iso] = resource_language.airtable_id

            if self._cache[iso] is None:
                continue

            resource_language_ids.add(self._cache[iso])

        return resource_language_ids
