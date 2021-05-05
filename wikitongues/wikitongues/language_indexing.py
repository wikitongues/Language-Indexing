#!/usr/bin/env python

# Entry point for the program, invoked from the console
import sys

from scrapy.crawler import CrawlerProcess
import os
import importlib

from config.load_configs import load_configs
from spiders.wikipedia_spider import WikipediaSpiderInput  # noqa: E501
from data_store.airtable.airtable_language_data_store_factory import AirtableLanguageDataStoreFactory  # noqa: E501
from data_store.airtable.airtable_connection_info import AirtableConnectionInfo
from data_store.airtable.airtable_table_info import AirtableTableInfo

# Info required to connect to Airtable
# TODO read from config file
base_id = ''
api_key = ''
table_name = 'Languages'
id_column = 'Identifier'

connection_info = AirtableConnectionInfo(base_id, api_key)
table_info = AirtableTableInfo(table_name, id_column)

# Get a LanguageDataStore instance
# fake=True will give us a fake data store that returns a sample set of
#   languages and does not require Airtable credentials
language_data_store = AirtableLanguageDataStoreFactory.get_data_store(
    connection_info, table_info, fake=True)

# Configure a CrawlerProcess
process = CrawlerProcess(
    settings={
        "FEEDS": {
            "items.jl": {
                "format": "jl"
            }
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

            process.crawl(spider_class, spider_input, language_data_store)
            process.start()


config = load_configs()
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
