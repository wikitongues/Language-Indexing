from abc import ABC, abstractmethod


class LanguageDataStore(ABC):

    @abstractmethod
    def get_language(self, iso_code):
        pass

    @abstractmethod
    def get_languages(self, iso_codes):
        pass

    @abstractmethod
    def list_languages(self, page_size, offset, max_records):
        pass
