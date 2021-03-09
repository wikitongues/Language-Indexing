from wikitongues.wikitongues.data_store.airtable.airtable_http_client import AirtableHttpClient  # noqa: E501
from wikitongues.wikitongues.data_store.airtable.airtable_connection_info import AirtableConnectionInfo  # noqa: E501

import responses
import unittest

BASE_ID = 'base_id'
API_KEY = 'api_key'
TABLE = 'MyTable'


class TestAirtableHttpClient(unittest.TestCase):
    def setUp(self):
        connection_info = AirtableConnectionInfo(BASE_ID, API_KEY)
        self.client = AirtableHttpClient(connection_info, TABLE)

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

        # headers = {
        #     'Authorization': f'Bearer {API_KEY}'
        # }

        responses.add(responses.GET, url, body=text)

        result = self.client.list_records(
            page_size=page_size, offset=offset, max_records=max_records)

        self.assertEqual(result.text, text)
