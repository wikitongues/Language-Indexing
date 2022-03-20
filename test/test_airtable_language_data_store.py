import json
import unittest

from language_indexing.data_store.airtable.airtable_http_client import IAirtableHttpClient
from language_indexing.data_store.airtable.airtable_language_data_store import AirtableLanguageDataStore
from language_indexing.data_store.airtable.airtable_language_extractor import IAirtableLanguageExtractor
from language_indexing.data_store.response_object import ResponseObject
from language_indexing.language import Language

EXPECTED_JSON = '{"records": [{"a": "a"}]}'
EXPECTED_JSON_1 = '{"records": [{"b": "b"}]}'
EXPECTED_NULL_JSON = '{"records": []}'

EXPECTED_LANGUAGE = Language("aaa", "Ghotuo", "https://en.wikipedia.org/wiki/Ghotuo_language")

EXPECTED_LANGUAGE_1 = Language("aac", "Ari", "https://en.wikipedia.org/wiki/Ari_language")

EXPECTED_ID = "aaa"
EXPECTED_ID_1 = "aac"
NULL_ID = "zzz"


class MockAirtableHttpClient(IAirtableHttpClient):
    def list_records(self, page_size, offset, max_records):
        return MockResponse()

    def get_record(self, id):
        if id == NULL_ID:
            return MockResponse(EXPECTED_NULL_JSON)
        elif id == EXPECTED_ID_1:
            return MockResponse(EXPECTED_JSON_1)

        return MockResponse()

    def get_records_by_fields(self, fields):
        pass

    def create_record(self, fields):
        pass


class MockAirtableLanguageExtractor(IAirtableLanguageExtractor):
    def extract_languages_from_json(self, json_obj, *args):
        result = ResponseObject()

        if len(json_obj["records"]) == 0:
            result.data = []
        elif json.dumps(json_obj) == EXPECTED_JSON_1:
            result.data = [EXPECTED_LANGUAGE_1]
        else:
            result.data = [EXPECTED_LANGUAGE]

        return result

    def extract_language_from_json(self, *args):
        pass


class MockResponse:
    def __init__(self, text=EXPECTED_JSON, status_code=200):
        self.text = text
        self.status_code = status_code


class TestAirtableLanguageDataStore(unittest.TestCase):
    def setUp(self):
        http_client = MockAirtableHttpClient()
        language_extractor = MockAirtableLanguageExtractor()
        self.data_store = AirtableLanguageDataStore(http_client, language_extractor)

    def test_list_languages(self):
        result = self.data_store.list_languages()

        self.assertIn(EXPECTED_LANGUAGE, result.data)

    def test_get_language(self):
        result = self.data_store.get_language(EXPECTED_ID)

        self.assertEqual(EXPECTED_LANGUAGE, result.data)

    def test_get_language__null_id(self):
        result = self.data_store.get_language(NULL_ID)

        self.assertIsNone(result.data)
        self.assertFalse(result.has_error())

    def test_get_languages(self):
        result = self.data_store.get_languages([EXPECTED_ID, EXPECTED_ID_1])

        self.assertEqual(2, len(result.data))
        self.assertEqual(EXPECTED_LANGUAGE, result.data[0])
        self.assertEqual(EXPECTED_LANGUAGE_1, result.data[1])
