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

        if response.status_code != 200:
            result.add_message(
                f'Airtable API request to get language \'{iso_code}\''
                f'returned status code {response.status_code}')
            return result

        json_obj = json.loads(response.text)
        extract_result = self._extractor.extract_languages_from_json(json_obj)

        if extract_result.has_error():
            return extract_result

        languages = extract_result.data

        if len(languages) == 0:
            return result

        result.data = languages[0]
        return result

    def get_languages(self, iso_codes):
        pass

    def list_languages(self):
        result = ErrorResponse()

        response = self._client.list_records()

        if response.status_code != 200:
            result.add_message(
                'Airtable API request to list languages returned status '
                f'code {response.status_code}')
            return result

        json_obj = json.loads(response.text)
        extract_result = self._extractor.extract_languages_from_json(json_obj)

        return extract_result
