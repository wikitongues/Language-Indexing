#!/usr/bin/env python

# Entry point for the program, invoked from the console
import sys

from scrapy.crawler import CrawlerProcess
import os
import importlib
from config.load_configs import load_configs
from spiders.wikipedia_spider import WikipediaSpiderInput  # noqa: E501
from data_store.airtable.airtable_language_data_store_factory import AirtableLanguageDataStoreFactory  # noqa: E501
from data_store.airtable.airtable_item_data_store_factory import AirtableItemDataStoreFactory  # noqa: E501
from data_store.airtable.airtable_connection_info import AirtableConnectionInfo
from data_store.airtable.airtable_table_info import AirtableTableInfo

# load config for running the spiders
config = load_configs()
# Info required to connect to Airtable
config_languages_table = config['airtable_languages_table']
config_item_table = config['airtable_items_table']

# Get a LanguageDataStore instance
# fake=True will give us a fake data store that returns a sample set of
#   languages and does not require Airtable credentials
# TODO check base_id and api_key are valid before creating the objects.

languages_data_store = AirtableLanguageDataStoreFactory.get_data_store(
    AirtableConnectionInfo(
        config_languages_table['base_id'], config_languages_table['api_key']),
    AirtableTableInfo(
        config_languages_table['table_name'], config_languages_table['id_column']),
    config_languages_table.getboolean('fake'))
item_data_store = AirtableItemDataStoreFactory.get_data_store(
    AirtableConnectionInfo(
        config_item_table['base_id'], config_item_table['api_key']),
    AirtableTableInfo(
        config_item_table['table_name'], config_item_table['id_column']),
    config_item_table.getboolean('fake'))


# Get an ItemDataStore instance
# fake=True will give us a fake data store that does not require Airtable
#   credentials

# Configure a CrawlerProcess
process = CrawlerProcess(
    settings={
        "FEEDS": {
            "items.jl": {
                "format": "jl"
            }
        },
        'ITEM_DATA_STORE': item_data_store,
        'ITEM_PIPELINES': {
            'pipelines.WikitonguesPipeline': 300
        }
    }
)


def process_site(site_tuple):
    iso_codes = [iso[1] for iso in config.items('language_codes')]

    spiders_dir_tree = os.listdir('wikitongues/wikitongues/spiders')

    for t in spiders_dir_tree:
        if t.__contains__(site_tuple[0]):
            spider_class = getattr(
                importlib.import_module(
                    'spiders.' + t[:-3]), config['spiders'][site_tuple[0]])

            spider_input = WikipediaSpiderInput(iso_codes)

            process.crawl(spider_class, spider_input, languages_data_store)
            process.start()


sites = config.items('sites')

start_all_crawls = input('Do you wish to crawl all spiders? (Y/N) ')

if start_all_crawls.lower() == 'n':
    site_to_crawl = input('Which site would you like to crawl? ')
    for site in sites:
        if site_to_crawl == site[0]:
            process_site(site_to_crawl)
            break
    print('Invalid input: could not find a site that matched your input')
    sys.exit(1)

elif start_all_crawls.lower() == 'y':
    for site in sites:
        process_site(site)
        print(site[1])

else:
    print('invalid input')
    sys.exit(1)
