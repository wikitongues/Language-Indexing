from types import ModuleType, SimpleNamespace
import unittest
from unittest import mock

from scrapy.crawler import CrawlerProcess

import config.config_keys as keys
from language_indexing_config import LanguageIndexingConfiguration, Title
from language_indexing_runner import LanguageIndexingRunner
from wikitongues.wikitongues.spiders.wikipedia_spider import WikipediaSpider

MODULE_UNDER_TEST = 'language_indexing_runner'

WIKIPEDIA_KEY = 'wikipedia'
WIKIPEDIA_SPIDER_CLASS = 'WikipediaSpider'


class TestLanguageIndexingRunner(unittest.TestCase):
    def setUp(self) -> None:
        self.configs = SimpleNamespace()
        self.configs.main_config = LanguageIndexingConfiguration()
        setattr(self.configs.main_config, keys.SPIDERS_SECTION, Title())
        setattr(self.configs.main_config[keys.SPIDERS_SECTION], WIKIPEDIA_KEY, WIKIPEDIA_SPIDER_CLASS)

        self.mock_language_data_store = mock.Mock()
        self.configs.language_data_store = self.mock_language_data_store

        self.import_module_patcher = mock.patch(f'{MODULE_UNDER_TEST}.importlib.import_module')
        self.mock_import_module = self.import_module_patcher.start()
        self.mock_spider_module = mock.MagicMock(ModuleType)
        self.mock_import_module.return_value = self.mock_spider_module

        self.mock_wikipedia_spider = mock.Mock()

        setattr(self.mock_spider_module, WIKIPEDIA_SPIDER_CLASS, WikipediaSpider)

        self.mock_wikipedia_spider_input = mock.Mock()

        def mock_get_spider_input(site, configs):
            if configs != self.configs:
                raise Exception

            if site == WIKIPEDIA_KEY:
                return self.mock_wikipedia_spider_input

            raise Exception

        self.spider_input_factory_patcher = mock.patch(f'{MODULE_UNDER_TEST}.SpiderInputFactory.get_spider_input')
        self.mock_get_spider_input = self.spider_input_factory_patcher.start()
        self.mock_get_spider_input.side_effect = mock_get_spider_input

        self.mock_process = mock.Mock(CrawlerProcess)

        def mock_get_crawler_process(configs):
            if configs != self.configs:
                raise Exception

            return self.mock_process

        self.crawler_process_factory_patcher = mock.patch(
            f'{MODULE_UNDER_TEST}.CrawlerProcessFactory.get_crawler_process'
        )
        self.mock_get_crawler_process = self.crawler_process_factory_patcher.start()
        self.mock_get_crawler_process.side_effect = mock_get_crawler_process

        self.mock_resource_language_service = mock.Mock()

        def mock_get_resource_language_service(configs):
            if configs != self.configs:
                raise Exception

            return self.mock_resource_language_service

        self.resource_language_service_factory_patcher = mock.patch(
            f'{MODULE_UNDER_TEST}.ResourceLanguageServiceFactory.get_resource_language_service'
        )
        self.mock_get_resource_language_service = self.resource_language_service_factory_patcher.start()
        self.mock_get_resource_language_service.side_effect = mock_get_resource_language_service

    def tearDown(self) -> None:
        self.import_module_patcher.stop()
        self.spider_input_factory_patcher.stop()
        self.crawler_process_factory_patcher.stop()
        self.resource_language_service_factory_patcher.stop()

    def test_process_site(self):
        LanguageIndexingRunner.process_site(WIKIPEDIA_KEY, self.configs)

        self.mock_process.crawl.assert_called_once_with(
            WikipediaSpider,
            spider_input=self.mock_wikipedia_spider_input,
            language_data_store=self.mock_language_data_store,
            resource_language_service=self.mock_resource_language_service
        )

        self.mock_process.start.assert_called_once()
