from wikitongues.wikitongues.data_store.airtable.airtable_language_data_store import AirtableLanguageDataStore  # noqa: E501
from wikitongues.wikitongues.data_store.airtable.airtable_http_client import IAirtableHttpClient  # noqa: E501
from wikitongues.wikitongues.data_store.airtable.airtable_language_extractor import IAirtableLanguageExtractor  # noqa: E501

from wikitongues.wikitongues.language import Language

import unittest

EXPECTED_JSON = '{"records": [{"a": "a"}]}'
EXPECTED_NULL_JSON = '{"records": []}'

EXPECTED_LANGUAGE = Language(
    'aaa',
    'Ghotuo',
    'https://en.wikipedia.org/wiki/Ghotuo_language')

EXPECTED_ID = 'aaa'
NULL_ID = 'zzz'


class MockAirtableHttpClient(IAirtableHttpClient):
    def list_records(self):
        return MockResponse()

    def get_record(self, id):
        if id == NULL_ID:
            return MockResponse(EXPECTED_NULL_JSON)

        return MockResponse()


class MockAirtableLanguageExtractor(IAirtableLanguageExtractor):
    def extract_languages_from_json(self, json_obj, *args):
        if len(json_obj['records']) == 0:
            return []

        return [EXPECTED_LANGUAGE]

    def extract_language_from_json(self, *args):
        pass


class MockResponse:
    def __init__(self, text=EXPECTED_JSON):
        self.text = text


class TestAirtableLanguageDataStore(unittest.TestCase):
    def setUp(self):
        http_client = MockAirtableHttpClient()
        language_extractor = MockAirtableLanguageExtractor()
        self.data_store = AirtableLanguageDataStore(
            http_client, language_extractor)

    def test_list_languages(self):
        result = self.data_store.list_languages()

        self.assertIn(EXPECTED_LANGUAGE, result)

    def test_get_language(self):
        result = self.data_store.get_language(EXPECTED_ID)

        self.assertEqual(EXPECTED_LANGUAGE, result)

    def test_get_language__null_id(self):
        result = self.data_store.get_language(NULL_ID)

        self.assertIsNone(result)
