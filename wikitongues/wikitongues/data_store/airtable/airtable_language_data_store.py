from ..language_data_store import LanguageDataStore
from ..error_response import ErrorResponse
import json


class AirtableLanguageDataStore(LanguageDataStore):

    def __init__(self, http_client, language_extractor):
        self._client = http_client
        self._extractor = language_extractor

    def get_language(self, iso_code):
        result = ErrorResponse()

        response = self._client.get_record(iso_code)

        json_obj = json.loads(response.text)
        languages = self._extractor.extract_languages_from_json(json_obj)

        if len(languages) == 0:
            return result

        result.data = languages[0]
        return result

    def get_languages(self, iso_codes):
        pass

    def list_languages(self):
        result = ErrorResponse()

        response = self._client.list_records()
        json_obj = json.loads(response.text)
        result.data = self._extractor.extract_languages_from_json(json_obj)
        return result
