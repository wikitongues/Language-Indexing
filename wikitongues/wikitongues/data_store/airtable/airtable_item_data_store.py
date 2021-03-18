from ..item_data_store import ItemDataStore
import json


class AirtableItemDataStore(ItemDataStore):

    def __init__(self, http_client, item_extractor, item_formatter):
        self._client = http_client
        self._extractor = item_extractor
        self._formatter = item_formatter

    def get_item(self, url):
        response = self._client.get_record(url)

        json_obj = json.loads(response.text)
        items = self._extractor.extract_items_from_json(json_obj)

        if len(items) == 0:
            return None

        return items[0]

    def create_item(self, item):
        fields = self._formatter.get_fields_dict(item)

        response = self._client.create_record(fields)

        return response.status_code == 200

    def update_item(self, item):
        pass
