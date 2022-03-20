import unittest
from types import SimpleNamespace
from unittest import mock

from language_indexing.crawler_process_factory import CrawlerProcessFactory


class TestCrawlerProcessFactory(unittest.TestCase):
    def test_get_crawler_process(self):
        configs = SimpleNamespace()
        configs.external_resource_data_store = mock.Mock()

        process = CrawlerProcessFactory.get_crawler_process(configs)

        settings = process.settings

        self.assertEqual(
            configs.external_resource_data_store,
            settings["EXTERNAL_RESOURCE_DATA_STORE"],
        )
        self.assertIn("language_indexing.pipelines.WikitonguesPipeline", settings["ITEM_PIPELINES"])
        self.assertIn("script", settings["METAREFRESH_IGNORE_TAGS"])
        self.assertIn("noscript", settings["METAREFRESH_IGNORE_TAGS"])
