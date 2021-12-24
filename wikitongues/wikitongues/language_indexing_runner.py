from spider_input_factory import SpiderInputFactory
import config.config_keys as keys
from lang_to_iso_converter import LangToIsoConverter
from resource_language_service import ResourceLanguageService

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
                'EXTERNAL_RESOURCE_DATA_STORE': configs.external_resource_datastore,
                'ITEM_PIPELINES': {
                    'pipelines.WikitonguesPipeline': 300
                },
                'METAREFRESH_IGNORE_TAGS': ['script', 'noscript']
            }
        )

        language_data_store = configs.languages_datastore
        lang_to_iso_converter = LangToIsoConverter()
        resource_language_service = ResourceLanguageService(language_data_store, lang_to_iso_converter)

        process.crawl(
            spider_class,
            spider_input=spider_input,
            language_data_store=language_data_store,
            resource_language_service=resource_language_service)

        process.start()
