from ..language_data_store import LanguageDataStore
from ..error_response import ErrorResponse
from language import Language


class FakeLanguageDataStore(LanguageDataStore):
    def get_language(self, iso_code):
        pass

    def get_languages(self, iso_codes):
        result = ErrorResponse()

        languages = [
            Language('sah', 'Sakha', 'https://en.wikipedia.org/wiki/Yakut_language'),  # noqa: E501
            Language('nrf', 'Jèrriais', 'https://en.wikipedia.org/wiki/J%C3%A8rriais'),  # noqa: E501
            Language('qwe', 'Quechua', 'https://en.wikipedia.org/wiki/Quechuan_languages'),  # noqa: E501
            Language('nys', 'Nyungar', 'https://en.wikipedia.org/wiki/Nyungar_language'),  # noqa: E501
            Language('xho', 'Xhosa', 'https://en.wikipedia.org/wiki/Xhosa_language'),  # noqa: E501
            Language('dak', 'Sioux', 'https://en.wikipedia.org/wiki/Sioux_language')  # noqa: E501
        ]

        result.data = languages
        return result

    def list_languages(self):
        pass
