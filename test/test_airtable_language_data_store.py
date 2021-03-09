from wikitongues.wikitongues.data_store.airtable.airtable_language_data_store import AirtableLanguageDataStore  # noqa: E501
from wikitongues.wikitongues.data_store.airtable.airtable_http_client import IAirtableHttpClient  # noqa: E501
from wikitongues.wikitongues.data_store.airtable.airtable_language_extractor import IAirtableLanguageExtractor  # noqa: E501

from wikitongues.wikitongues.language import Language

import unittest

EXPECTED_JSON = {}

EXPECTED_LANGUAGE = Language(
    'aaa',
    'Ghotuo',
    'https://en.wikipedia.org/wiki/Ghotuo_language')


class MockAirtableHttpClient(IAirtableHttpClient):
    def list_records(self):
        return MockResponse()


class MockAirtableLanguageExtractor(IAirtableLanguageExtractor):
    def extract_languages_from_json(self, *args):
        return [EXPECTED_LANGUAGE]

    def extract_language_from_json(self, *args):
        pass


class MockResponse:
    json_obj = EXPECTED_JSON


class TestAirtableLanguageDataStore(unittest.TestCase):
    def setUp(self):
        http_client = MockAirtableHttpClient()
        language_extractor = MockAirtableLanguageExtractor()
        self.data_store = AirtableLanguageDataStore(
            http_client, language_extractor)

    def test_list_languages(self):
        result = self.data_store.list_languages()

        self.assertIn(EXPECTED_LANGUAGE, result)
