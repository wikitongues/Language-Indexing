#!/usr/bin/env python

# Entry point for the program, invoked from the console
import sys

from scrapy.crawler import CrawlerProcess
import os
import importlib
from config.load_configs import load_main_config, \
    load_item_airtable_datastores, load_languages_airtable_datastores, \
    read_exclude_languages, read_include_languages
from spiders.wikipedia_spider import WikipediaSpiderInput

# load config for running the spiders
config = load_main_config()
# Info required to connect to Airtable
item_datastore = load_item_airtable_datastores(config)
languages_datastore = load_languages_airtable_datastores(config)
# load languages table
config_languages_table = config['airtable_languages_table']

# Configure a CrawlerProcess
process = CrawlerProcess(
    settings={
        "FEEDS": {
            "items.jl": {
                "format": "jl"
            }
        },
        'ITEM_DATA_STORE': item_datastore,
        'ITEM_PIPELINES': {
            'pipelines.WikitonguesPipeline': 300
        }
    }
)


def process_site(site_tuple):

    current_dir = os.path.dirname(__file__)
    spiders_dir_tree = os.listdir(os.path.join(current_dir, 'spiders'))

    for t in spiders_dir_tree:
        if t.__contains__(site_tuple[0]):
            spider_class = getattr(
                importlib.import_module(
                    'spiders.' + t[:-3]), config['spiders'][site_tuple[0]])

            spider_input = WikipediaSpiderInput(read_include_languages(config),
                                                read_exclude_languages(config),
                                                config_languages_table['page_size'],
                                                config_languages_table['offset'],
                                                config_languages_table['max_records']
                                                )

            process.crawl(spider_class, spider_input, languages_datastore)
            process.start()


sites = config.items('sites')

start_all_crawls = input('Do you wish to crawl all spiders? (Y/N) ')

if start_all_crawls.lower() == 'n':
    site_to_crawl = input('Which site would you like to crawl? ')
    for site in sites:
        if site_to_crawl == site[0]:
            process_site(site)
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
