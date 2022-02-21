from typing import List, Optional

from ..data_store.airtable.airtable_connection_info import AirtableConnectionInfo
from ..data_store.airtable.airtable_external_resource_data_store_factory import (
    AirtableExternalResourceDataStoreFactory,
)
from ..data_store.airtable.airtable_language_data_store_factory import (
    AirtableLanguageDataStoreFactory,
)
from ..data_store.airtable.airtable_table_info import AirtableTableInfo
from ..data_store.airtable.offset_utility import OffsetUtility
from ..data_store.external_resource_data_store import ExternalResourceDataStore
from ..data_store.language_data_store import LanguageDataStore
from ..language_indexing_config import LanguageIndexingConfiguration


def load_external_resource_airtable_config(config: LanguageIndexingConfiguration) -> ExternalResourceDataStore:

    config_external_resource_table = config["airtable_external_resources_table"]

    # TODO check base_id and api_key are valid before creating the objects.

    # Get a ExternalResourceDataStore instance
    # fake=True will give us a fake data store that returns a sample set of
    #   languages and does not require Airtable credentials
    external_resource_data_store = AirtableExternalResourceDataStoreFactory.get_data_store(
        AirtableConnectionInfo(
            config_external_resource_table["base_id"],
            config_external_resource_table["api_key"],
        ),
        AirtableTableInfo(
            config_external_resource_table["table_name"],
            config_external_resource_table["id_column"],
            config_external_resource_table["page_size"],
            OffsetUtility.read_offset(),
            config_external_resource_table["max_records"],
        ),
        eval(config_external_resource_table["fake"].capitalize()),
    )
    return external_resource_data_store


def load_languages_airtable_config(config: LanguageIndexingConfiguration) -> LanguageDataStore:

    config_languages_table = config["airtable_languages_table"]
    # Get a LanguageDataStore instance
    # fake=True will give us a fake data store that returns a sample set of
    #   languages and does not require Airtable credentials
    language_data_store = AirtableLanguageDataStoreFactory.get_data_store(
        AirtableConnectionInfo(config_languages_table["base_id"], config_languages_table["api_key"]),
        AirtableTableInfo(
            config_languages_table["table_name"],
            config_languages_table["id_column"],
            config_languages_table["page_size"],
            OffsetUtility.read_offset(),
            config_languages_table["max_records"],
        ),
        eval(config_languages_table["fake"].capitalize()),
    )
    return language_data_store


def read_include_languages(config: LanguageIndexingConfiguration) -> Optional[List[str]]:
    if hasattr(config, "include_languages") and len(config["include_languages"].__dict__) > 0:
        return config["include_languages"]["include_languages"].split(",")
    return None


def read_exclude_languages(config: LanguageIndexingConfiguration) -> Optional[List[str]]:
    if hasattr(config, "exclude_languages") and len(config["exclude_languages"].__dict__) > 0:
        return config["exclude_languages"]["exclude_languages"].split(",")
    return None
