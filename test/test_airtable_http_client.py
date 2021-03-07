from wikitongues.wikitongues.data_store.airtable.airtable_http_client import AirtableHttpClient
from wikitongues.wikitongues.data_store.airtable.airtable_connection_info import AirtableConnectionInfo

import pytest
import requests
import requests_mock

BASE_ID = 'base_id'
API_KEY = 'api_key'
TABLE = 'MyTable'

@pytest.fixture
def connection_info():
    return AirtableConnectionInfo(BASE_ID, API_KEY)

@pytest.fixture
def client(connection_info):
    return AirtableHttpClient(connection_info, TABLE)

def test_list_records(client):
    text = 'expected text'
    page_size = 3
    offset = 'rec123'
    max_records = 10
    url = f'https://api.airtable.com/v0/{BASE_ID}/{TABLE}?maxRecords={max_records}&pageSize={page_size}&offset={offset}'

    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    with requests_mock.Mocker() as m:
        m.get(url, headers=headers, text=text)

    result = client.list_records(page_size=page_size, offset=offset, max_records=max_records)

    assert result.text == text
