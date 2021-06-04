from ..language_data_store import LanguageDataStore
from ..error_response import ErrorResponse
from .offset_utility import OffsetUtility
import json


class AirtableLanguageDataStore(LanguageDataStore):
    """
    Performs actions on an Airtable base for language data

    Args:
        LanguageDataStore
    """

    def __init__(self, http_client, language_extractor):
        """
        Construct AirtableLanguageDataStore

        Args:
            http_client (IAirtableHttpClient): Http client
            language_extractor (IAirtableLanguageExtractor): Language extractor
        """

        self._client = http_client
        self._extractor = language_extractor

    def get_language(self, iso_code):
        """
        Retrieves language object for the given ISO code

        Args:
            iso_code (str): ISO code

        Returns:
            ErrorResponse: Response object containing Language object
        """

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
        """
        Retrieves language objects for the given ISO codes

        Args:
            iso_codes (list): List of ISO codes

        Returns:
            ErrorResponse: Response object containing list of Language objects
        """

        languages = []

        for iso_code in iso_codes:
            result = self.get_language(iso_code)

            if result.has_error():
                return result

            languages.append(result.data)

        result = ErrorResponse()
        result.data = languages
        return result

    def list_languages(self, page_size=100, max_records=None, **kwargs):
        """
        Retrieves list of language objects

        Returns:
            ErrorResponse: Response object containing list of Language objects
        """

        result = ErrorResponse()

        response = self._client.list_records(
            page_size, kwargs.get('offset'), max_records)

        if response.status_code != 200:
            result.add_message(
                'Airtable API request to list languages returned status '
                f'code {response.status_code}')
            return result

        json_obj = json.loads(response.text)
        extract_result = self._extractor.extract_languages_from_json(json_obj)
        OffsetUtility.write_offset(json_obj.get('offset'))

        return extract_result
