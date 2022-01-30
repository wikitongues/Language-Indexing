import unittest
from logging import Logger
from unittest import mock

from scrapy.exceptions import DropItem

from wikitongues.wikitongues.data_store.error_response import ErrorResponse
from wikitongues.wikitongues.data_store.external_resource_data_store import (
    ExternalResourceDataStore,
)
from wikitongues.wikitongues.items import ExternalResource
from wikitongues.wikitongues.pipelines import WikitonguesPipeline

MODULE_UNDER_TEST = "wikitongues.wikitongues.pipelines"

EXPECTED_URL = "https://termcoord.eu/2015/05/discovering-mirandese/"
EXPECTED_ISO = "mwl"


class TestPipelines(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_external_resource_data_store = mock.Mock(ExternalResourceDataStore)

        self.get_logger_patcher = mock.patch(f"{MODULE_UNDER_TEST}.logging.getLogger")
        mock_get_logger = self.get_logger_patcher.start()
        self.mock_logger = mock.Mock(Logger)
        mock_get_logger.return_value = self.mock_logger

        self.pipeline = WikitonguesPipeline(self.mock_external_resource_data_store)

        self.mock_external_resource = mock.Mock(ExternalResource)

        def mock_get(field_name, *_):
            if field_name == "url":
                return EXPECTED_URL
            elif field_name == "iso_code":
                return EXPECTED_ISO

            raise Exception

        self.mock_external_resource.get.side_effect = mock_get

    def tearDown(self) -> None:
        self.get_logger_patcher.stop()

    def test_duplicate_no_iso__drop_item(self):
        def mock_get_external_resource(url, iso_code):
            result = mock.Mock(ErrorResponse)
            result.data = None
            if url == EXPECTED_URL and iso_code == "":
                result.data = mock.ANY
            return result

        self.mock_external_resource_data_store.get_external_resource.side_effect = mock_get_external_resource

        mock_external_resource = mock.Mock(ExternalResource)

        def mock_get(field_name, default_value=""):
            if field_name == "url":
                return EXPECTED_URL
            elif field_name == "iso_code":
                return default_value

            raise Exception

        mock_external_resource.get.side_effect = mock_get

        mock_spider = mock.ANY

        with self.assertRaisesRegex(DropItem, f"Resource already indexed: {EXPECTED_URL}"):
            self.pipeline.process_item(mock_external_resource, mock_spider)

        self.mock_external_resource_data_store.create_external_resource.assert_not_called()

    def test_duplicate_with_iso__drop_item(self):
        def mock_get_external_resource(url, iso_code):
            result = mock.Mock(ErrorResponse)
            result.data = None
            if url == EXPECTED_URL and iso_code == EXPECTED_ISO:
                result.data = mock.ANY
            return result

        self.mock_external_resource_data_store.get_external_resource.side_effect = mock_get_external_resource

        mock_spider = mock.ANY

        with self.assertRaisesRegex(
            DropItem,
            f"Resource already indexed for language {EXPECTED_ISO}: {EXPECTED_URL}",
        ):
            self.pipeline.process_item(self.mock_external_resource, mock_spider)

        self.mock_external_resource_data_store.create_external_resource.assert_not_called()

    def test_create_item_success(self):
        def mock_get_external_resource(*_):
            result = mock.Mock(ErrorResponse)
            result.data = None
            return result

        self.mock_external_resource_data_store.get_external_resource.side_effect = mock_get_external_resource

        def mock_create_external_resource(*_):
            result = mock.Mock(ErrorResponse)
            result.has_error.return_value = False
            return result

        self.mock_external_resource_data_store.create_external_resource.side_effect = mock_create_external_resource

        mock_spider = mock.ANY

        result = self.pipeline.process_item(self.mock_external_resource, mock_spider)

        self.assertEqual(self.mock_external_resource, result)

        self.mock_external_resource_data_store.create_external_resource.assert_called_once_with(
            self.mock_external_resource
        )

    def test_create_item_error__logs(self):
        def mock_get_external_resource(*_):
            result = mock.Mock(ErrorResponse)
            result.data = None
            return result

        self.mock_external_resource_data_store.get_external_resource.side_effect = mock_get_external_resource

        expected_errors = ["line1", "line2"]

        def mock_create_external_resource(*_):
            result = mock.Mock(ErrorResponse)
            result.has_error.return_value = True
            result.messages = expected_errors
            return result

        self.mock_external_resource_data_store.create_external_resource.side_effect = mock_create_external_resource

        mock_spider = mock.ANY

        self.pipeline.process_item(self.mock_external_resource, mock_spider)

        self.mock_logger.error.assert_called_once_with("\n".join(expected_errors))
