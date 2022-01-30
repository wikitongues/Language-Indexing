import json
import unittest

import wikitongues.wikitongues.data_store.airtable.field_name as field_name
from wikitongues.wikitongues.data_store.airtable.airtable_external_resource_data_store import (
    AirtableExternalResourceDataStore,
)
from wikitongues.wikitongues.data_store.airtable.airtable_external_resource_extractor import (
    IAirtableExternalResourceExtractor,
)
from wikitongues.wikitongues.data_store.airtable.airtable_external_resource_formatter import (
    IAirtableExternalResourceFormatter,
)
from wikitongues.wikitongues.data_store.airtable.airtable_http_client import (
    IAirtableHttpClient,
)
from wikitongues.wikitongues.data_store.error_response import ErrorResponse
from wikitongues.wikitongues.items import ExternalResource

EXPECTED_URL = "aaa.com"
EXPECTED_ISO = "aaa"
EXPECTED_NULL_URL = "newsite.com/notyetcrawled"
EXPECTED_JSON = '{"records": [{"a": "a"}]}'
EXPECTED_NULL_JSON = '{"records": []}'

EXPECTED_RESOURCE = ExternalResource(title="Title", url="aaa.com", language_id="aaa", spider_name="test")

EXPECTED_FIELDS = {"Title": "Title", "Url": "aaa.com", "Language": ["rec12345"]}


class MockAirtableHttpClient(IAirtableHttpClient):
    def list_records(self):
        return MockResponse()

    def get_record(self, id):
        pass

    def get_records_by_fields(self, fields):
        if fields[field_name.ISO_FIELD] == EXPECTED_ISO and fields[field_name.URL_FIELD] == EXPECTED_URL:
            return MockResponse(EXPECTED_JSON)

        return MockResponse()

    def create_record(self, fields):
        if fields == EXPECTED_FIELDS:
            return MockResponse()

        return MockResponse(status_code=500)


class MockAirtableExternalResourceExtractor(IAirtableExternalResourceExtractor):
    def extract_external_resources_from_json(self, json_obj, *args):
        result = ErrorResponse()

        if len(json_obj["records"]) == 0:
            result.data = []
        elif json.dumps(json_obj) == EXPECTED_JSON:
            result.data = [EXPECTED_RESOURCE]

        return result

    def extract_external_resource_from_json(self, json_obj):
        pass


class MockAirtableExternalResourceFormatter(IAirtableExternalResourceFormatter):
    def get_fields_dict(self, external_resource):
        if external_resource == EXPECTED_RESOURCE:
            return EXPECTED_FIELDS

        return {}


class MockResponse:
    def __init__(self, text=EXPECTED_NULL_JSON, status_code=200):
        self.text = text
        self.status_code = status_code


class TestAirtableExternalResourceDataStore(unittest.TestCase):
    def setUp(self):
        http_client = MockAirtableHttpClient()
        external_resource_extractor = MockAirtableExternalResourceExtractor()
        external_resource_formatter = MockAirtableExternalResourceFormatter()
        self.data_store = AirtableExternalResourceDataStore(
            http_client, external_resource_extractor, external_resource_formatter
        )

    def test_get_external_resource(self):
        result = self.data_store.get_external_resource(EXPECTED_URL, EXPECTED_ISO)

        self.assertEqual(EXPECTED_RESOURCE, result.data)

    def test_get_external_resource__null_id(self):
        result = self.data_store.get_external_resource(EXPECTED_NULL_URL, EXPECTED_ISO)

        self.assertIsNone(result.data)
        self.assertFalse(result.has_error())

    def test_create_external_resource(self):
        result = self.data_store.create_external_resource(EXPECTED_RESOURCE)

        self.assertFalse(result.has_error())
