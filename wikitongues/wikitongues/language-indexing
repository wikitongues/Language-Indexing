#!/usr/bin/env python

# Entry point for the program, invoked from the console

from scrapy.crawler import CrawlerProcess
import configparser
import os
import importlib

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources  # noqa: F401

from spiders.wikipedia_spider import WikipediaSpiderInput  # noqa: E501
from data_store.airtable.airtable_language_data_store_factory import AirtableLanguageDataStoreFactory  # noqa: E501
from data_store.airtable.airtable_connection_info import AirtableConnectionInfo
from data_store.airtable.airtable_table_info import AirtableTableInfo

import config as config_pkg

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
    iso_codes = [iso[1] for iso in config['language_codes']]

    spiders_dir_tree = os.listdir('wikitongues/wikitongues/spiders')

    for t in spiders_dir_tree:
        if t.__contains__(site_tuple[0]):
            spider_class = getattr(
                importlib.import_module(
                    'spiders.' + t[:-3]), config['spiders'][site_tuple[0]])

            spider_input = WikipediaSpiderInput(iso_codes)

            process.crawl(spider_class, spider_input, language_data_store)
            process.start()


config_text = pkg_resources.read_text(config_pkg, 'indexing.cfg')
config = configparser.ConfigParser()
config.read_string(config_text)
sites = config.items('sites')
start_all_crawls = input('Do you wish to crawl all spiders? (Y/N) ')
#start_all_crawls = 'y'
if start_all_crawls.lower() == 'n':
    site_to_crawl = input('Which site would you like to crawl? ')
    for site in sites:
        if site_to_crawl == site[0]:
            process_site(site_to_crawl)
            break
    print('Invalid input: could not find a site that matched your input')

elif start_all_crawls.lower() == 'y':
    for site in sites:
        process_site(site)
        print(site[1])

else:
    print('invalid input')
