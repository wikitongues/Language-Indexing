import importlib
from types import SimpleNamespace

from inflection import underscore

from .config import config_keys as keys
from .crawler_process_factory import CrawlerProcessFactory
from .resource_language_service_factory import ResourceLanguageServiceFactory
from .spider_input_factory import SpiderInputFactory

_SPIDERS_MODULE = ".spiders"


class LanguageIndexingRunner:
    @staticmethod
    def process_site(site: str, configs: SimpleNamespace) -> None:
        process = CrawlerProcessFactory.get_crawler_process(configs)

        spider_class_name = configs.main_config[keys.SPIDERS_SECTION][site]
        spider_module_name = f"{_SPIDERS_MODULE}.{underscore(spider_class_name)}"
        spider_class = getattr(importlib.import_module(spider_module_name, package=__package__), spider_class_name)

        spider_input = SpiderInputFactory.get_spider_input(site, configs)
        language_data_store = configs.language_data_store
        resource_language_service = ResourceLanguageServiceFactory.get_resource_language_service(configs)

        process.crawl(
            spider_class,
            spider_input=spider_input,
            language_data_store=language_data_store,
            resource_language_service=resource_language_service,
        )

        process.start()
