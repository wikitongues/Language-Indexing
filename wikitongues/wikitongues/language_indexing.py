#!/usr/bin/env python
# Entry point for the program, invoked from the console
import sys
import types

from scrapy.crawler import CrawlerProcess
import importlib
from inflection import underscore

from config.load_configs import \
    load_item_airtable_datastores, load_languages_airtable_datastores
from spider_input_factory import SpiderInputFactory
from write_user_config import ask_user_for_user_file_creation
from language_indexing_config import LanguageIndexingConfiguration, load_config


def main():
    configs = types.SimpleNamespace()

    # Instantiate configuration object
    configs.main_config = LanguageIndexingConfiguration()

    ask_user_for_user_file_creation()

    start = input('Begin the web crawling process? (Y/N) ')
    if start.lower() == 'n':
        sys.exit(0)

    load_config(configs.main_config)
    # The load_config function will try to read user file
    # as long as there is two arguments passed
    load_config(configs.main_config, 'user_config')

    # Info required to connect to Airtable
    configs.item_datastore = load_item_airtable_datastores(configs.main_config)
    configs.languages_datastore = \
        load_languages_airtable_datastores(configs.main_config)
    # load languages table
    configs.config_languages_table = \
        configs.main_config['airtable_languages_table']
    # Configure a CrawlerProcess
    process = CrawlerProcess(
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

    def process_site(site):
        spider_class_name = configs.main_config['spiders'][site]
        spider_module_name = f'spiders.{underscore(spider_class_name)}'

        spider_class = getattr(
            importlib.import_module(spider_module_name),
            spider_class_name)

        spider_input = SpiderInputFactory.get_spider_input(site, configs)

        process.crawl(
            spider_class,
            spider_input=spider_input,
            language_data_store=configs.languages_datastore)

        process.start()

    sites = configs.main_config['sites']

    # start_all_crawls = input('Do you wish to crawl all spiders? (Y/N) ')

    # if start_all_crawls.lower() == 'n':
    #     site_to_crawl = input('Which site would you like to crawl? ')
    #     for site in sites:
    #         if site_to_crawl == site[0]:
    #             process_site(site)
    #             break
    #     print('Invalid input: could not find a site that matched your input')
    #     sys.exit(1)

    # elif start_all_crawls.lower() == 'y':
    for site in sites.__dict__:
        process_site(site)

    # else:
    #     print('invalid input')
    #     sys.exit(1)
