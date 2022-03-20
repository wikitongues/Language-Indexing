#!/usr/bin/env python
# Entry point for the program, invoked from the console
import sys
import types

from .config import config_keys as keys
from .config.load_configs import load_external_resource_airtable_config, load_languages_airtable_config
from .language_indexing_config import LanguageIndexingConfiguration, load_config
from .language_indexing_runner import LanguageIndexingRunner
from .write_user_config import ask_user_for_user_file_creation


def main() -> None:
    configs = types.SimpleNamespace()

    ask_user_for_user_file_creation()

    start = input("Begin the web crawling process? (Y/N) ")
    if start.lower() == "n":
        sys.exit(0)

    configure(configs)

    sites = configs.main_config[keys.SITES_SECTION].__dict__.keys()

    print("Enter site to target:")

    for site in sites:
        print(f"* {site}")

    site = None
    while site is None:
        site_input = input()
        site = next((site for site in sites if site_input.lower() == site.lower()), None)

        if site is None:
            print(f'Unrecognized site "{site_input}"')

    try:
        LanguageIndexingRunner.process_site(site, configs)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def configure(configs: types.SimpleNamespace) -> None:
    # Instantiate configuration object
    configs.main_config = LanguageIndexingConfiguration()

    # Read default config
    load_config(configs.main_config)

    # Read user config
    load_config(configs.main_config, "user_config")

    configs.external_resource_data_store = load_external_resource_airtable_config(configs.main_config)

    configs.language_data_store = load_languages_airtable_config(configs.main_config)

    configs.config_languages_table = configs.main_config[keys.AIRTABLE_LANGUAGES_TABLE_SECTION]
