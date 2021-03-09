from abc import ABC, abstractmethod
import requests


class IAirtableHttpClient(ABC):
    @abstractmethod
    def list_records(self, page_size=None, offset=None, max_records=100):
        pass


class AirtableHttpClient(IAirtableHttpClient):

    _base_url = 'https://api.airtable.com/v0'

    def __init__(self, connection_info, table):

        self._route = '/'.join([
            self._base_url,
            connection_info.base_id,
            table
        ])

        self._headers = {
            'Authorization': f'Bearer {connection_info.api_key}'
        }

    def list_records(self, page_size=None, offset=None, max_records=100):
        params = [
            f'maxRecords={max_records}'
        ]

        if page_size is not None:
            params.append(f'pageSize={page_size}')

        if offset is not None:
            params.append(f'offset={offset}')

        url = f'{self._route}?{"&".join(params)}'

        return requests.get(url, headers=self._headers)
