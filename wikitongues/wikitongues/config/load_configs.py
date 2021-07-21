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


def load_main_config():

    print("loading config file")

    default_config = configparser.ConfigParser(allow_no_value=True)
    current_dir = os.path.dirname(__file__)
    default_config.read_file(open(os.path.join(current_dir, "indexing.cfg")))
    local_config_file = default_config["local_config_file"]

    user_config = configparser.ConfigParser(allow_no_value=True)

    if platform == "windows" or platform == "win32":
        env = os.getenv("APPDATA")
    elif platform == "linux" or platform == "linux2" or platform == "darwin":
        env = os.getenv("HOME")
    else:
        raise Exception("This program is intended only for Mac,"
                        + "Linux, or Windows machines.")

    user_config_path = os.sep.join([env, local_config_file['file_name']])

    try:
        user_config_file = open(user_config_path)
        user_config.read_file(user_config_file)
        user_config_file.close()
        pass
    except FileNotFoundError:
        print("Error: User config file not found at path " + user_config_path)
        sys.exit(1)
        pass

    if len(user_config.items("sites")) > 0:
        # override sites configuration
        print("Using user configuration")
        return user_config
    else:
        # nothing overridden. return the default config settings
        print("Using default configuration")
        return default_config


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
        eval(config_item_table['fake'].capitalize()))
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
        eval(config_languages_table['fake'].capitalize()))
    return languages_datastore


def read_include_languages(config):
    if hasattr(config, 'include_languages') and \
            len(config["include_languages"].__dict__) > 0:
        return config['include_languages']['include_languages'].split(",")
    return None


def read_exclude_languages(config):
    if hasattr(config, 'exclude_languages') and \
            len(config["exclude_languages"].__dict__) > 0:
        return config['exclude_languages']['exclude_languages'].split(",")
    return None
