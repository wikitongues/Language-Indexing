#!/usr/bin/env python

# Entry point for the program, invoked from the console
import sys
import types

from scrapy.crawler import CrawlerProcess
import os
import importlib
from config.load_configs import load_main_config, \
    load_item_airtable_datastores, load_languages_airtable_datastores, \
    read_exclude_languages, read_include_languages
from spiders.wikipedia_spider import WikipediaSpiderInput


def main():

    # load config for running the spiders
    configs = types.SimpleNamespace()
    configs.main_config = load_main_config()
    # Info required to connect to Airtable
    configs.item_datastore = load_item_airtable_datastores(configs.main_config)
    configs.languages_datastore = load_languages_airtable_datastores(configs.main_config)
    # load languages table
    configs.config_languages_table = configs.main_config['airtable_languages_table']

    # Configure a CrawlerProcess
    configs.process = CrawlerProcess(
        settings={
            "FEEDS": {
                "items.jl": {
                    "format": "jl"
                }
            },
            'ITEM_DATA_STORE': configs.item_datastore,
            'ITEM_PIPELINES': {
                'pipelines.WikitonguesPipeline': 300
            }
        }
    )

    sites = configs.main_config.items('sites')

    start_all_crawls = input('Do you wish to crawl all spiders? (Y/N) ')

    if start_all_crawls.lower() == 'n':
        site_to_crawl = input('Which site would you like to crawl? ')
        for site in sites:
            if site_to_crawl == site[0]:
                process_site(site, configs)
                break
        print('Invalid input: could not find a site that matched your input')
        sys.exit(1)

    elif start_all_crawls.lower() == 'y':
        for site in sites:
            process_site(site, configs)
            print(site[1])

    else:
        print('invalid input')
        sys.exit(1)


def process_site(site_tuple, configs):

    current_dir = os.path.dirname(__file__)
    spiders_dir_tree = os.listdir(os.path.join(current_dir, 'spiders'))

    for t in spiders_dir_tree:
        if t.__contains__(site_tuple[0]):
            spider_class = getattr(
                importlib.import_module(
                    'spiders.' + t[:-3]), configs.main_config['spiders'][site_tuple[0]])

            spider_input = WikipediaSpiderInput(read_include_languages(configs.main_config),
                                                read_exclude_languages(configs.main_config),
                                                configs.config_languages_table
                                                ['page_size'],
                                                configs.config_languages_table
                                                ['offset'],
                                                configs.config_languages_table
                                                ['max_records']
                                                )

            configs.process.crawl(spider_class, spider_input, configs.languages_datastore)
            configs.process.start()



