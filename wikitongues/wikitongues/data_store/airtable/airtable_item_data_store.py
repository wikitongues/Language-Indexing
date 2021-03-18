from ..item_data_store import ItemDataStore
from ..error_response import ErrorResponse
import json


class AirtableItemDataStore(ItemDataStore):

    def __init__(self, http_client, item_extractor, item_formatter):
        self._client = http_client
        self._extractor = item_extractor
        self._formatter = item_formatter

    def get_item(self, url):
        result = ErrorResponse()

        response = self._client.get_record(url)

        json_obj = json.loads(response.text)
        items = self._extractor.extract_items_from_json(json_obj)

        if len(items) == 0:
            return result

        result.data = items[0]
        return result

    def create_item(self, item):
        result = ErrorResponse()

        fields = self._formatter.get_fields_dict(item)

        response = self._client.create_record(fields)

        if response.status_code != 200:
            result.add_message(
                'Airtable API request to create item returned status code '
                f'{response.status_code}')
            return result

        return result

    def update_item(self, item):
        pass
