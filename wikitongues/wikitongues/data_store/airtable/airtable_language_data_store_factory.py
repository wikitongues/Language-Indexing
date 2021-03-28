from .airtable_language_data_store import AirtableLanguageDataStore
from .airtable_http_client import AirtableHttpClient
from .airtable_language_extractor import AirtableLanguageExtractor


class AirtableLanguageDataStoreFactory:
    @staticmethod
    def get_data_store(connection_info, table_info):
        http_client = AirtableHttpClient(connection_info, table_info)
        language_extractor = AirtableLanguageExtractor()
        return AirtableLanguageDataStore(http_client, language_extractor)
