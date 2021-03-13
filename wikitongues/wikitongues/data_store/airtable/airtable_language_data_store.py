from ..language_data_store import LanguageDataStore
import json


class AirtableLanguageDataStore(LanguageDataStore):

    def __init__(self, http_client, language_extractor):
        self._client = http_client
        self._extractor = language_extractor

    def get_language(self, iso_code):
        response = self._client.get_record(iso_code)

        json_obj = json.loads(response.text)
        languages = self._extractor.extract_languages_from_json(json_obj)

        if len(languages) == 0:
            return None

        return languages[0]

    def get_languages(self, iso_codes):
        pass

    def list_languages(self):
        response = self._client.list_records()
        json_obj = json.loads(response.text)
        return self._extractor.extract_languages_from_json(json_obj)
