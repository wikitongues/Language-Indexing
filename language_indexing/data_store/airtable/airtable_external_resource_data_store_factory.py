from ..external_resource_data_store import ExternalResourceDataStore
from .airtable_connection_info import AirtableConnectionInfo
from .airtable_external_resource_data_store import AirtableExternalResourceDataStore
from .airtable_external_resource_extractor import AirtableExternalResourceExtractor
from .airtable_external_resource_formatter import AirtableExternalResourceFormatter
from .airtable_http_client import AirtableHttpClient
from .airtable_table_info import AirtableTableInfo
from .fake_external_resource_data_store import FakeExternalResourceDataStore


class AirtableExternalResourceDataStoreFactory:
    """
    Factory for providing external resource data store instances
    """

    @staticmethod
    def get_data_store(
        connection_info: AirtableConnectionInfo, table_info: AirtableTableInfo, fake: bool = False
    ) -> ExternalResourceDataStore:
        """
        Returns an external resource data store instance

        Args:
            connection_info (AirtableConnectionInfo): Airtable connection info
            table_info (AirtableTableInfo): Airtable table info
            fake (bool, optional): If true, a fake data store that does not \
require Airtable credentials is returned. Defaults to False.

        Returns:
            ExternalResourceDataStore: External resource data store instance
        """

        if fake:
            return FakeExternalResourceDataStore()

        http_client = AirtableHttpClient(connection_info, table_info)
        external_resource_extractor = AirtableExternalResourceExtractor()
        external_resource_formatter = AirtableExternalResourceFormatter()
        return AirtableExternalResourceDataStore(http_client, external_resource_extractor, external_resource_formatter)
