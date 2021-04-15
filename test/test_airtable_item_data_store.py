from wikitongues.wikitongues.data_store.airtable.airtable_item_data_store import AirtableItemDataStore  # noqa: E501
from wikitongues.wikitongues.data_store.airtable.airtable_http_client import IAirtableHttpClient  # noqa: E501
from wikitongues.wikitongues.data_store.airtable.airtable_item_id_provider import AirtableItemIdProvider  # noqa: E501
from wikitongues.wikitongues.data_store.airtable.airtable_item_formatter import IAirtableItemFormatter  # noqa: E501
from wikitongues.wikitongues.data_store.airtable.airtable_item_extractor import IAirtableItemExtractor  # noqa: E501

from wikitongues.wikitongues.data_store.error_response import ErrorResponse

from wikitongues.wikitongues.items import WikitonguesItem

import unittest
import json

EXPECTED_URL = 'aaa.com'
EXPECTED_ISO = 'aaa'
EXPECTED_NULL_URL = 'newsite.com/notyetcrawled'
EXPECTED_JSON = '{"records": [{"a": "a"}]}'
EXPECTED_NULL_JSON = '{"records": []}'

EXPECTED_ITEM = WikitonguesItem(
    title='Title',
    url='aaa.com',
    language_id='aaa',
    spider_name='test'
)

EXPECTED_FIELDS = {
    'Title': 'Title',
    'Url': 'aaa.com',
    'Language': [
        'rec12345'
    ]
}


class MockAirtableHttpClient(IAirtableHttpClient):
    def list_records(self):
        return MockResponse()

    def get_record(self, id):
        if id == f'{EXPECTED_ISO}:{EXPECTED_URL}':
            return MockResponse(EXPECTED_JSON)

        return MockResponse()

    def create_record(self, fields):
        if fields == EXPECTED_FIELDS:
            return MockResponse()

        return MockResponse(status_code=500)


class MockAirtableItemExtractor(IAirtableItemExtractor):
    def extract_items_from_json(self, json_obj, *args):
        result = ErrorResponse()

        if len(json_obj['records']) == 0:
            result.data = []
        elif json.dumps(json_obj) == EXPECTED_JSON:
            result.data = [EXPECTED_ITEM]

        return result

    def extract_item_from_json(self, json_obj):
        pass


class MockAirtableItemFormatter(IAirtableItemFormatter):
    def get_fields_dict(self, item):
        if item == EXPECTED_ITEM:
            return EXPECTED_FIELDS

        return {}


class MockResponse:
    def __init__(self, text=EXPECTED_NULL_JSON, status_code=200):
        self.text = text
        self.status_code = status_code


class TestAirtableItemDataStore(unittest.TestCase):
    def setUp(self):
        http_client = MockAirtableHttpClient()
        item_extractor = MockAirtableItemExtractor()
        item_formatter = MockAirtableItemFormatter()
        id_provider = AirtableItemIdProvider()
        self.data_store = AirtableItemDataStore(
            http_client, item_extractor, item_formatter, id_provider)

    def test_get_item(self):
        result = self.data_store.get_item(EXPECTED_URL, EXPECTED_ISO)

        self.assertEqual(EXPECTED_ITEM, result.data)

    def test_get_item__null_id(self):
        result = self.data_store.get_item(EXPECTED_NULL_URL, EXPECTED_ISO)

        self.assertIsNone(result.data)
        self.assertFalse(result.has_error())

    def test_create_item(self):
        result = self.data_store.create_item(EXPECTED_ITEM)

        self.assertFalse(result.has_error())
