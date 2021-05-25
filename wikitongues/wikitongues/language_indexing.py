#!/usr/bin/env python

# Entry point for the program, invoked from the console
import re
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

# Info required to connect to Airtable
config = load_configs()
# TODO read from config file
config_connection_info = config.items('airtable_connection_info')
config_table_info = config.items('airtable_table_info')
config_languages_table_items = config.items('airtable_languages_table')
config_item_table_items = config.items('airtable_items_table')
base_id = ''
api_key = ''
connection_info = ''
languages_table_items = ''
items_table_items = ''

if config_connection_info.getboolean('fake'):
    connection_info = AirtableConnectionInfo('base_id, api_key')
else:
    connection_info = AirtableConnectionInfo(config_connection_info['base_id'], config_connection_info['api_key'])
    # table_info = AirtableTableInfo(config_connection_info['name'], config_connection_info['id_column'])

# Get a LanguageDataStore instance
# fake=True will give us a fake data store that returns a sample set of
#   languages and does not require Airtable credentials
m = re.search('[{}<>]', config_languages_table_items['base_id'])
languages_table_info = AirtableTableInfo(
    config_table_info['name'], config_table_info['id_column'])
items_table_info = AirtableTableInfo(
    config_table_info['name'], config_table_info['id_column'])
languages_data_store = AirtableLanguageDataStoreFactory.get_data_store(
    connection_info,
    languages_table_info,
    config_languages_table_items.getboolean('fake'))
item_data_store = AirtableItemDataStoreFactory.get_data_store(
    connection_info,
    items_table_info,
    config_item_table_items.getboolean('fake'))

# if len(config_languages_table_items['base_id']) > 0 and len(m) is 0:
#    language_data_store = AirtableLanguageDataStoreFactory.get_data_store(
#    connection_info, table_info, fake=True)

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
