#!/usr/bin/env python

# Entry point for the program, invoked from the console
import sys

from scrapy.crawler import CrawlerProcess
import os
import importlib
from config.load_configs import load_main_config, \
    load_item_airtable_datastores, load_languages_airtable_datastores
from spiders.wikipedia_spider import WikipediaSpiderInput

class LanguageIndexingConfiguration:
    def __getitem__(self,key):
        return getattr(self,key)

# Save each section of the config as a object
class Title:
    pass

# Read in default properties
def load_config(config, default_config_file_name = None):
    try:
        #Default case: when nothing is passed, the program reads the default config
        if default_config_file_name == None:
            load_config(config, "config/indexing.cfg")

        else:
            #When a user file in the same directory is passed, read that file
            default_config = open(os.path.join(sys.path[0], default_config_file_name), "r")
            if (default_config == None):
                print("file not found")
            title = Title()
            name = None
            for line in default_config:
                # Do nothing if it is a comment or empty line
                if line.startswith("#") or line.startswith('\n'):
                    continue
                # Save the name for the section
                elif line.startswith("["):
                    # When reach a new section, save everything before it into config
                    if name != None:
                        setattr(config, name, title)
                    name = line[1: -2]
                    title = Title()
                # Save each individual data under the section
                else:
                    word = line.split(" : ")
                    # If there is no value for the key
                    if len(word) == 1:
                        setattr(title, word[0].rstrip(), None)
                    # If there is value for the key
                    else:
                        setattr(title, word[0], word[1].rstrip())
            setattr(config, name, title)
            default_config.close()

    except IOError:
        print("File does not exist.")
        sys.exit(1)


# Instantiate configuration object
config = LanguageIndexingConfiguration()

load_config(config)

# load config for running the spiders
# config = load_main_config()

# Info required to connect to Airtable
item_datastore = load_item_airtable_datastores(config)
languages_datastore = load_languages_airtable_datastores(config)

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
    iso_codes = [
        iso for iso in list(config._sections['language_codes'].values())
    ]

    current_dir = os.path.dirname(__file__)
    spiders_dir_tree = os.listdir(os.path.join(current_dir, 'spiders'))

    for t in spiders_dir_tree:
        if t.__contains__(site_tuple[0]):
            spider_class = getattr(
                importlib.import_module(
                    'spiders.' + t[:-3]), config['spiders'][site_tuple[0]])

            spider_input = WikipediaSpiderInput(iso_codes)

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
