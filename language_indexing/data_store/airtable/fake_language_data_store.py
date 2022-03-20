from typing import List

from ...language import Language
from ..language_data_store import LanguageDataStore
from ..response_object import ResponseObject

LANGUAGES = [
    Language("sah", "Sakha", "https://en.wikipedia.org/wiki/Yakut_language"),
    Language("nrf", "Jèrriais", "https://en.wikipedia.org/wiki/J%C3%A8rriais"),
    Language("qwe", "Quechua", "https://en.wikipedia.org/wiki/Quechuan_languages"),
    Language("nys", "Nyungar", "https://en.wikipedia.org/wiki/Nyungar_language"),
    Language("xho", "Xhosa", "https://en.wikipedia.org/wiki/Xhosa_language"),
    Language("dak", "Sioux", "https://en.wikipedia.org/wiki/Sioux_language"),
    Language("mwl", "Mirandese", "https://en.wikipedia.org/wiki/Mirandese_language"),
]


class FakeLanguageDataStore(LanguageDataStore):
    def get_language(self, iso_code: str) -> ResponseObject[Language]:
        result = ResponseObject()

        for language in LANGUAGES:
            if language.id == iso_code:
                result.data = language
                break

        return result

    def get_languages(self, iso_codes: List[str]) -> ResponseObject[List[Language]]:
        result = ResponseObject()

        result.data = filter(lambda language: language.id in iso_codes, LANGUAGES)

        return result

    def list_languages(self) -> ResponseObject[List[Language]]:
        return self.get_languages(None)
