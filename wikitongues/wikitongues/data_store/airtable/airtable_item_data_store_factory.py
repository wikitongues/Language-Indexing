from .airtable_item_data_store import AirtableItemDataStore
from .airtable_http_client import AirtableHttpClient
from .airtable_item_extractor import AirtableItemExtractor
from .airtable_item_formatter import AirtableItemFormatter
from .airtable_item_id_provider import AirtableItemIdProvider
from .fake_item_data_store import FakeItemDataStore


class AirtableItemDataStoreFactory:
    """
    Factory for providing item data store instances
    """

    @staticmethod
    def get_data_store(connection_info, table_info, fake=False):
        """
        Returns an item data store instance

        Args:
            connection_info (AirtableConnectionInfo): Airtable connection info
            table_info (AirtableTableInfo): Airtable table info
            fake (bool, optional): If true, a fake data store that does not \
require Airtable credentials is returned. Defaults to False.

        Returns:
            ItemDataStore: Item data store instance
        """

        if fake:
            return FakeItemDataStore()

        http_client = AirtableHttpClient(connection_info, table_info)
        item_extractor = AirtableItemExtractor()
        item_formatter = AirtableItemFormatter()
        id_provider = AirtableItemIdProvider()
        return AirtableItemDataStore(
            http_client, item_extractor, item_formatter, id_provider)
