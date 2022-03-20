import unittest
from unittest import mock

from scrapy.http.response.html import HtmlResponse
from scrapy.selector import SelectorList

from language_indexing.language import Language
from language_indexing.resource_language_service import IResourceLanguageService
from language_indexing.spiders.util.wikipedia_util import WikipediaUtil

MODULE_UNDER_TEST = "language_indexing.spiders.util.wikipedia_util"

EXPECTED_EXTERNAL_LINK_SELECTOR = "a.external.text"
EXPECTED_LINK_TEXT_SELECTOR = "::text"
EXPECTED_SPIDER_NAME = "wikipedia"

BAD_LINK = "https://en.wikipedia.org/w/index.php?title=Template:Romance_languages&action=edit"
GOOD_LINK_1 = "https://www.ethnologue.com/18/language/mwl/"
GOOD_LINK_2 = "https://termcoord.eu/2015/05/discovering-mirandese/"

TEXT_1 = "Mirandese"
TEXT_2 = "Discovering Mirandese"
BAD_LINK_TEXT = "E"


def get_mock_link(url, text):
    mock_link = mock.Mock(SelectorList)
    mock_link.attrib = {"href": url}

    def mock_css(selector):
        if selector != EXPECTED_LINK_TEXT_SELECTOR:
            raise Exception

        mock_css_result = mock.Mock(SelectorList)
        mock_css_result.get.return_value = text
        return mock_css_result

    mock_link.css.side_effect = mock_css
    return mock_link


class TestWikipediaUtil(unittest.TestCase):
    def test_parse_wikipedia_page(self):
        response = mock.Mock(HtmlResponse)

        def mock_css(selector):
            if selector != EXPECTED_EXTERNAL_LINK_SELECTOR:
                raise Exception

            links = [
                get_mock_link(BAD_LINK, BAD_LINK_TEXT),
                get_mock_link(GOOD_LINK_1, TEXT_1),
                get_mock_link(GOOD_LINK_2, TEXT_2),
            ]

            return links

        response.css = mock.Mock()
        response.css.side_effect = mock_css

        language = mock.Mock(Language)
        resource_language_service = mock.Mock(IResourceLanguageService)
        spider_name = "test"

        result = WikipediaUtil.parse_wikipedia_page(response, language, resource_language_service, spider_name)

        urls = set()
        for external_link_request in result:
            urls.add(external_link_request.url)

        self.assertEqual(2, len(urls))
        self.assertIn(GOOD_LINK_1, urls)
        self.assertIn(GOOD_LINK_2, urls)
        self.assertNotIn(BAD_LINK, urls)
