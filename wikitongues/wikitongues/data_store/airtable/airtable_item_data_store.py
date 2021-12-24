from ..item_data_store import ItemDataStore
from ..error_response import ErrorResponse
from . import field_name
import json


class AirtableItemDataStore(ItemDataStore):
    """
    Performs actions on an Airtable base for crawled items
    """

    def __init__(
            self, http_client, item_extractor, item_formatter):
        """
        Construct AirtableItemDataStore

        Args:
            http_client (IAirtableHttpClient): Airtable Http Client instance
            item_extractor (IAirtableItemExtractor): Airtable Item Extractor instance
            item_formatter (IAirtableItemFormatter): Airtable Item Formater instance
        """
        self._client = http_client
        self._extractor = item_extractor
        self._formatter = item_formatter

    def get_item(self, url, iso_code):
        """
        Get item

        Args:
            url (str): Url of item
            iso_code (str): ISO code of associated language

        Returns:
            ErrorResponse: Response object with item
        """

        result = ErrorResponse()

        response = self._client.get_records_by_fields({
            field_name.URL_FIELD: url,
            field_name.ISO_FIELD: iso_code
        })

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
        """
        Create item in data store

        Args:
            item (WikitonguesItem): WikitonguesItem object

        Returns:
            ErrorRespone: Response object
        """

        result = ErrorResponse()

        fields = self._formatter.get_fields_dict(item)

        response = self._client.create_record(fields)

        if response.status_code != 200:
            result.add_message(
                'Airtable API request to create item returned status code '
                f'{response.status_code}')
            result.add_message(response.text)
            return result

        return result
