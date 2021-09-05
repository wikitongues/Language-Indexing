from spider_input_factory import SpiderInputFactory
import config.config_keys as keys

from scrapy.crawler import CrawlerProcess
import importlib
from inflection import underscore


class LanguageIndexingRunner:
    @staticmethod
    def process_site(site, configs):
        spider_class_name = configs.main_config[keys.SPIDERS_SECTION][site]
        spider_module_name = f'spiders.{underscore(spider_class_name)}'

        spider_class = getattr(
            importlib.import_module(spider_module_name),
            spider_class_name)

        spider_input = SpiderInputFactory.get_spider_input(site, configs)

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

        process.crawl(
            spider_class,
            spider_input=spider_input,
            language_data_store=configs.languages_datastore)

        process.start()
