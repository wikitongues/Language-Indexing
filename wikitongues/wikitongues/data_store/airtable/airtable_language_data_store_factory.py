from .airtable_language_data_store import AirtableLanguageDataStore
from .airtable_http_client import AirtableHttpClient
from .airtable_language_extractor import AirtableLanguageExtractor
from .fake_language_data_store import FakeLanguageDataStore


class AirtableLanguageDataStoreFactory:
    """
    Factory for providing language data store instances
    """

    @staticmethod
    def get_data_store(connection_info, table_info, fake=False):
        """
        Returns a language data store instance

        Args:
            connection_info (AirtableConnectionInfo): Airtable connection info
            table_info (AirtableTableInfo): Airtable table info
            fake (bool, optional): If true, a fake data store with sample \
language data, not requiring Airtable credentials, is returned. Defaults to \
False.

        Returns:
            LanguageDataStore: Language data store instance
        """

        if fake:
            return FakeLanguageDataStore()

        http_client = AirtableHttpClient(connection_info, table_info)
        language_extractor = AirtableLanguageExtractor()
        return AirtableLanguageDataStore(http_client, language_extractor)
