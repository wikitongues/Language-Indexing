#!/usr/bin/env python
# Entry point for the program, invoked from the console
import sys
import types

from language_indexing_runner import LanguageIndexingRunner

from config.load_configs import \
    load_item_airtable_datastores, load_languages_airtable_datastores
from write_user_config import ask_user_for_user_file_creation
from language_indexing_config import LanguageIndexingConfiguration, load_config

import config.config_keys as keys


def main():
    configs = types.SimpleNamespace()

    ask_user_for_user_file_creation()

    start = input('Begin the web crawling process? (Y/N) ')
    if start.lower() == 'n':
        sys.exit(0)

    configure(configs)

    sites = configs.main_config[keys.SITES_SECTION]

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
        LanguageIndexingRunner.process_site(site, configs)

    # else:
    #     print('invalid input')
    #     sys.exit(1)


def configure(configs):
    # Instantiate configuration object
    configs.main_config = LanguageIndexingConfiguration()

    # Read default config
    load_config(configs.main_config)

    # Read user config
    load_config(configs.main_config, 'user_config')

    configs.item_datastore = load_item_airtable_datastores(configs.main_config)

    configs.languages_datastore = load_languages_airtable_datastores(
        configs.main_config)

    configs.config_languages_table = \
        configs.main_config[keys.AIRTABLE_LANGUAGES_TABLE_SECTION]
