import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

from language_indexing.config.logging_settings import LoggingSettings
from language_indexing.crawler_process_factory import CrawlerProcessFactory

MODULE_UNDER_TEST = "language_indexing.crawler_process_factory"


class TestCrawlerProcessFactory(unittest.TestCase):
    @mock.patch(f"{MODULE_UNDER_TEST}.abspath")
    @mock.patch(f"{MODULE_UNDER_TEST}.read_logging_settings")
    def test_get_crawler_process(self, mock_read_logging_settings, mock_abspath):
        configs = SimpleNamespace()
        configs.external_resource_data_store = mock.Mock()
        configs.main_config = mock.Mock()

        expected_log_file = "~/language-indexing.log"
        expected_log_file_append = True
        expected_log_level = "INFO"

        mock_read_logging_settings.return_value = mock.Mock(
            LoggingSettings,
            log_file=expected_log_file,
            log_file_append=expected_log_file_append,
            log_level=expected_log_level,
        )

        with tempfile.NamedTemporaryFile() as fp:
            expected_abspath = fp.name
            mock_abspath.return_value = expected_abspath

            process = CrawlerProcessFactory.get_crawler_process(configs)

        settings = process.settings

        self.assertEqual(
            configs.external_resource_data_store,
            settings["EXTERNAL_RESOURCE_DATA_STORE"],
        )
        self.assertEqual(expected_abspath, settings["LOG_FILE"])
        self.assertEqual(expected_log_file_append, settings["LOG_FILE_APPEND"])
        self.assertEqual(expected_log_level, settings["LOG_LEVEL"])
        self.assertIn("language_indexing.pipelines.WikitonguesPipeline", settings["ITEM_PIPELINES"])
        self.assertIn("script", settings["METAREFRESH_IGNORE_TAGS"])
        self.assertIn("noscript", settings["METAREFRESH_IGNORE_TAGS"])

        mock_read_logging_settings.assert_called_once_with(configs.main_config)
        mock_abspath.assert_called_once_with(expected_log_file)
