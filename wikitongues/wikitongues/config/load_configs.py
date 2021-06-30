import sys
from sys import platform
import configparser
import os

from data_store.airtable.airtable_connection_info \
    import AirtableConnectionInfo
from data_store.airtable.airtable_item_data_store_factory \
    import AirtableItemDataStoreFactory
from data_store.airtable.airtable_language_data_store_factory \
    import AirtableLanguageDataStoreFactory
from data_store.airtable.airtable_table_info import AirtableTableInfo
from data_store.airtable.offset_utility import OffsetUtility





def load_item_airtable_datastores(config):

    config_item_table = config['airtable_items_table']

    # TODO check base_id and api_key are valid before creating the objects.

    # Get a ItemDataStore instance
    # fake=True will give us a fake data store that returns a sample set of
    #   languages and does not require Airtable credentials
    item_datastore = AirtableItemDataStoreFactory.get_data_store(
        AirtableConnectionInfo(
            config_item_table['base_id'], config_item_table['api_key']),
        AirtableTableInfo(
            config_item_table['table_name'], config_item_table['id_column'],
            config_item_table['page_size'], OffsetUtility.read_offset(),
            config_item_table['max_records']),
        config_item_table.getboolean('fake'))
    return item_datastore


def load_languages_airtable_datastores(config):

    config_languages_table = config['airtable_languages_table']
    # Get a LanguageDataStore instance
    # fake=True will give us a fake data store that returns a sample set of
    #   languages and does not require Airtable credentials
    languages_datastore = AirtableLanguageDataStoreFactory.get_data_store(
        AirtableConnectionInfo(
            config_languages_table['base_id'],
            config_languages_table['api_key']),
        AirtableTableInfo(
            config_languages_table['table_name'],
            config_languages_table['id_column'],
            config_languages_table['page_size'],
            OffsetUtility.read_offset(),
            config_languages_table['max_records']),
        config_languages_table.getboolean('fake'))
    return languages_datastore


def read_include_languages(config):

    if len(config.items("include_languages")) > 0:
        return config['include_languages'].split(",")
    return None


def read_exclude_languages(config):

    if len(config.items("exclude_languages")) > 0:
        return config['exclude_languages'].split(",")
    return None
