import unittest
from unittest import mock

from responses import Response
from scrapy.http.response.html import HtmlResponse

from wikitongues.wikitongues.language import Language
from wikitongues.wikitongues.spiders.util.external_resource_parser import (
    ExternalResourceParser,
)

MODULE_UNDER_TEST = "wikitongues.wikitongues.spiders.util.external_resource_parser"

EXPECTED_LINK_TEXT = "The text of the link"
EXPECTED_SPIDER_NAME = "test"
EXPECTED_ISO_CODE = "aaa"
EXPECTED_LANGUAGE_ID = "rec1"
EXPECTED_TITLE = "The title of the page"
EXPECTED_TITLE_SELECTOR = "title::text"
EXPECTED_LANG_VALUES = {"aaa", "en"}
EXPECTED_RESOURCE_LANGUAGE_IDS = {"rec1", "rec2"}
EXPECTED_URL = "aaa.com"


class TestExternalResourceParser(unittest.TestCase):
    def setUp(self) -> None:
        self.response = mock.Mock(HtmlResponse)
        self.response.status = 200
        self.response.url = EXPECTED_URL

        def mock_css(selector):
            mock_css_result = mock.Mock()
            mock_css_result.get = mock.Mock(return_value=EXPECTED_TITLE)

            if selector == EXPECTED_TITLE_SELECTOR:
                return mock_css_result

            raise Exception

        self.response.css = mock.Mock()
        self.response.css.side_effect = mock_css

        self.language = mock.Mock(Language)
        self.language.id = EXPECTED_ISO_CODE
        self.language.airtable_id = EXPECTED_LANGUAGE_ID

        self.get_lang_values_patcher = mock.patch(f"{MODULE_UNDER_TEST}.LangAttributeParser.get_lang_values")
        self.mock_get_lang_values = self.get_lang_values_patcher.start()
        self.mock_get_lang_values.return_value = EXPECTED_LANG_VALUES

        self.resource_language_service = mock.Mock()
        self.resource_language_service.get_resource_language_ids.return_value = EXPECTED_RESOURCE_LANGUAGE_IDS

    def tearDown(self) -> None:
        self.get_lang_values_patcher.stop()

    def test_parse_external_link_not_200(self):
        status_codes = [400, 401, 404, 451, 500]
        for status_code in status_codes:
            response = mock.Mock()
            response.status = status_code

            with self.assertRaises(StopIteration):
                next(
                    ExternalResourceParser.parse_external_link(
                        response, EXPECTED_LINK_TEXT, mock.ANY, EXPECTED_SPIDER_NAME
                    )
                )

    def test_html_response_with_language(self):
        external_resource = next(
            ExternalResourceParser.parse_external_link(
                self.response,
                EXPECTED_LINK_TEXT,
                self.resource_language_service,
                EXPECTED_SPIDER_NAME,
                language=self.language,
            )
        )

        self.assertEqual(EXPECTED_TITLE, external_resource["title"])
        self.assertEqual(EXPECTED_LINK_TEXT, external_resource["link_text"])
        self.assertEqual(EXPECTED_URL, external_resource["url"])
        self.assertEqual(EXPECTED_ISO_CODE, external_resource["iso_code"])
        self.assertEqual(EXPECTED_LANGUAGE_ID, external_resource["language_id"])
        self.assertEqual(EXPECTED_SPIDER_NAME, external_resource["spider_name"])
        self.assertEqual(EXPECTED_RESOURCE_LANGUAGE_IDS, external_resource["resource_languages"])
        self.assertEqual(EXPECTED_LANG_VALUES, external_resource["resource_languages_raw"])

    def test_html_response_without_language(self):
        external_resource = next(
            ExternalResourceParser.parse_external_link(
                self.response,
                EXPECTED_LINK_TEXT,
                self.resource_language_service,
                EXPECTED_SPIDER_NAME,
            )
        )

        self.assertEqual(EXPECTED_TITLE, external_resource["title"])
        self.assertEqual(EXPECTED_LINK_TEXT, external_resource["link_text"])
        self.assertEqual(EXPECTED_URL, external_resource["url"])
        self.assertEqual(None, external_resource["iso_code"])
        self.assertEqual(None, external_resource["language_id"])
        self.assertEqual(EXPECTED_SPIDER_NAME, external_resource["spider_name"])
        self.assertEqual(EXPECTED_RESOURCE_LANGUAGE_IDS, external_resource["resource_languages"])
        self.assertEqual(EXPECTED_LANG_VALUES, external_resource["resource_languages_raw"])

    def test_non_html_with_language(self):
        response = mock.Mock(Response)
        response.status = 200
        response.url = EXPECTED_URL

        external_resource = next(
            ExternalResourceParser.parse_external_link(
                response,
                EXPECTED_LINK_TEXT,
                self.resource_language_service,
                EXPECTED_SPIDER_NAME,
                language=self.language,
            )
        )

        self.assertEqual(EXPECTED_LINK_TEXT, external_resource["title"])
        self.assertEqual(EXPECTED_LINK_TEXT, external_resource["link_text"])
        self.assertEqual(EXPECTED_URL, external_resource["url"])
        self.assertEqual(EXPECTED_ISO_CODE, external_resource["iso_code"])
        self.assertEqual(EXPECTED_LANGUAGE_ID, external_resource["language_id"])
        self.assertEqual(EXPECTED_SPIDER_NAME, external_resource["spider_name"])

    def test_non_html_without_language(self):
        response = mock.Mock(Response)
        response.status = 200
        response.url = EXPECTED_URL

        external_resource = next(
            ExternalResourceParser.parse_external_link(
                response,
                EXPECTED_LINK_TEXT,
                self.resource_language_service,
                EXPECTED_SPIDER_NAME,
            )
        )

        self.assertEqual(EXPECTED_LINK_TEXT, external_resource["title"])
        self.assertEqual(EXPECTED_LINK_TEXT, external_resource["link_text"])
        self.assertEqual(EXPECTED_URL, external_resource["url"])
        self.assertEqual(None, external_resource["iso_code"])
        self.assertEqual(None, external_resource["language_id"])
        self.assertEqual(EXPECTED_SPIDER_NAME, external_resource["spider_name"])
