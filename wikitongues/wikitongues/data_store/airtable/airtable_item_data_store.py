from ..item_data_store import ItemDataStore
from ..error_response import ErrorResponse
import json


class AirtableItemDataStore(ItemDataStore):

    def __init__(
            self, http_client, item_extractor, item_formatter, id_provider):
        self._client = http_client
        self._extractor = item_extractor
        self._formatter = item_formatter
        self._id_provider = id_provider

    def get_item(self, url, iso_code):
        result = ErrorResponse()

        item_id = self._id_provider.get_item_id(url, iso_code)
        response = self._client.get_record(item_id)

        json_obj = json.loads(response.text)
        extract_result = self._extractor.extract_items_from_json(json_obj)

        if extract_result.has_error():
            return extract_result

        items = extract_result.data

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
