from wikitongues.wikitongues.data_store.airtable.airtable_http_client import AirtableHttpClient
from wikitongues.wikitongues.data_store.airtable.airtable_connection_info import AirtableConnectionInfo
from wikitongues.wikitongues.data_store.airtable.airtable_table_info import AirtableTableInfo
import wikitongues.wikitongues.data_store.airtable.field_name as field_name

import responses
import unittest
import json

BASE_ID = 'base_id'
API_KEY = 'api_key'
TABLE = 'MyTable'
ID_COLUMN = 'Identifier'

CONNECTION_INFO = AirtableConnectionInfo(BASE_ID, API_KEY)
TABLE_INFO = AirtableTableInfo(TABLE, ID_COLUMN)


class TestAirtableHttpClient(unittest.TestCase):
    def setUp(self):
        self.client = AirtableHttpClient(CONNECTION_INFO, TABLE_INFO)

    @responses.activate
    def test_list_records(self):
        text = 'expected text'
        page_size = 3
        offset = 'rec123'
        max_records = 10
        url = (
            f'https://api.airtable.com/v0/{BASE_ID}/{TABLE}?'
            f'maxRecords={max_records}&pageSize={page_size}&offset={offset}'
        )

        def callback(request):
            if request.headers['Authorization'] != f'Bearer {API_KEY}':
                return (401, {}, None)

            return (200, {}, text)

        responses.add_callback(responses.GET, url, callback=callback)

        result = self.client.list_records(
            page_size=page_size, offset=offset, max_records=max_records)

        self.assertEqual(result.text, text)

    @responses.activate
    def test_get_record(self):
        text = 'expected text'
        id = 'id123'
        url = (
            f'https://api.airtable.com/v0/{BASE_ID}/{TABLE}?filterByFormula='
            f'FIND%28%27{id}%27%2C+%7B{ID_COLUMN}%7D%29+%21%3D+0'
        )

        def callback(request):
            if request.url != url:
                return (404, {}, None)

            if request.headers['Authorization'] != f'Bearer {API_KEY}':
                return (401, {}, None)

            return (200, {}, text)

        responses.add_callback(responses.GET, url, callback=callback)

        result = self.client.get_record(id)

        self.assertEqual(result.text, text)

    @responses.activate
    def test_get_records_by_fields(self):
        text = 'expected text'
        iso = 'sah'
        resource_url = 'http://www.baayaga.narod.ru'
        fields = {
            field_name.ISO_FIELD: iso,
            field_name.URL_FIELD: resource_url
        }
        url = (
            f'https://api.airtable.com/v0/{BASE_ID}/{TABLE}?filterByFormula='
            'AND%28%7BCoverage+%5BWeb%3A+Link%5D%7D%3D%27http%3A%2F%2Fwww.baayaga.narod.ru%27%2C%7BSubject+%5BISO+Code%5D%7D%3D%27sah%27%29'  # noqa: E501
        )

        def callback(request):
            if request.url != url:
                return (404, {}, None)

            if request.headers['Authorization'] != f'Bearer {API_KEY}':
                return (401, {}, None)

            return (200, {}, text)

        responses.add_callback(responses.GET, url, callback=callback)

        result = self.client.get_records_by_fields(fields)

        self.assertEqual(result.text, text)

    @responses.activate
    def test_get_records_by_fields__null_value(self):
        text = 'expected text'
        resource_url = 'http://www.baayaga.narod.ru'
        fields = {
            field_name.ISO_FIELD: None,
            field_name.URL_FIELD: resource_url
        }
        url = (
            f'https://api.airtable.com/v0/{BASE_ID}/{TABLE}?filterByFormula='
            'AND%28%7BCoverage+%5BWeb%3A+Link%5D%7D%3D%27http%3A%2F%2Fwww.baayaga.narod.ru%27%29'
        )

        def callback(request):
            if request.url != url:
                return (404, {}, None)

            if request.headers['Authorization'] != f'Bearer {API_KEY}':
                return (401, {}, None)

            return (200, {}, text)

        responses.add_callback(responses.GET, url, callback=callback)

        result = self.client.get_records_by_fields(fields)

        self.assertEqual(result.text, text)

    @responses.activate
    def test_create_record(self):
        text = 'expected text'
        url = f'https://api.airtable.com/v0/{BASE_ID}/{TABLE}'
        fields = {
            'a': 'a',
            'b': 'b',
            'c': 'c'
        }

        def callback(request):
            if request.headers['Authorization'] != f'Bearer {API_KEY}':
                return (401, {}, None)

            json_obj = json.loads(request.body)

            if type(json_obj['records']) != list:
                return (400, {}, None)

            if len(json_obj['records']) != 1:
                return (400, {}, None)

            if type(json_obj['records'][0]['fields']) != dict:
                return (400, {}, None)

            return (200, {}, text)

        responses.add_callback(responses.POST, url, callback=callback)

        result = self.client.create_record(fields)

        self.assertEqual(result.text, text)
