from types import SimpleNamespace
import unittest
from unittest import mock

import config.config_keys as keys
from language_indexing_config import LanguageIndexingConfiguration, Title
from spider_input_factory import SpiderInputFactory
from spiders.translated_site_spider import TranslatedSiteSpiderInput
from spiders.wikipedia_spider import WikipediaSpiderInput


MODULE_UNDER_TEST = 'spider_input_factory'

WIKIPEDIA_KEY = 'Wikipedia'
WIKIPEDIA_SPIDER_CLASS = 'WikipediaSpider'

BBC_KEY = 'BBC'
TRANSLATED_SITE_SPIDER_CLASS = 'TranslatedSiteSpider'
BBC_URL = 'https://www.bbc.com/ws/languages'
BBC_SELECTOR = '#english_version .units-list>li>a'

EXPECTED_PAGE_SIZE = 100
EXPECTED_MAX_RECORDS = 1000


class TestSpiderInputFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.configs = SimpleNamespace()
        self.configs.main_config = LanguageIndexingConfiguration()
        setattr(self.configs.main_config, keys.SPIDERS_SECTION, Title())
        setattr(self.configs.main_config[keys.SPIDERS_SECTION], WIKIPEDIA_KEY, WIKIPEDIA_SPIDER_CLASS)
        setattr(self.configs.main_config[keys.SPIDERS_SECTION], BBC_KEY, TRANSLATED_SITE_SPIDER_CLASS)

        self.configs.config_languages_table = Title()
        setattr(self.configs.config_languages_table, keys.PAGE_SIZE_KEY, EXPECTED_PAGE_SIZE)
        setattr(self.configs.config_languages_table, keys.MAX_RECORDS_KEY, EXPECTED_MAX_RECORDS)

        setattr(self.configs.main_config, keys.TRANSLATED_SITE_URLS_SECTION, Title())
        setattr(self.configs.main_config[keys.TRANSLATED_SITE_URLS_SECTION], BBC_KEY, BBC_URL)
        setattr(self.configs.main_config, keys.TRANSLATED_SITE_SELECTORS_SECTION, Title())
        setattr(self.configs.main_config[keys.TRANSLATED_SITE_SELECTORS_SECTION], BBC_KEY, BBC_SELECTOR)

    @mock.patch(f'{MODULE_UNDER_TEST}.OffsetUtility.read_offset')
    @mock.patch(f'{MODULE_UNDER_TEST}.read_exclude_languages')
    @mock.patch(f'{MODULE_UNDER_TEST}.read_include_languages')
    def test_wikipedia(self, mock_read_include_languages, mock_read_exclude_languages, mock_read_offset):
        expected_include_languages = ['sah', 'xho']
        expected_exclude_languages = ['eng', 'spa']

        def mock_read_include_languages_side_effect(main_config):
            if main_config == self.configs.main_config:
                return expected_include_languages

            raise Exception

        def mock_read_exclude_languages_side_effect(main_config):
            if main_config == self.configs.main_config:
                return expected_exclude_languages

            raise Exception

        mock_read_include_languages.side_effect = mock_read_include_languages_side_effect
        mock_read_exclude_languages.side_effect = mock_read_exclude_languages_side_effect

        expected_offset = 'offset'
        mock_read_offset.return_value = expected_offset

        wikipedia_spider_input = SpiderInputFactory.get_spider_input(WIKIPEDIA_KEY, self.configs)

        self.assertIsInstance(wikipedia_spider_input, WikipediaSpiderInput)
        self.assertListEqual(expected_include_languages, wikipedia_spider_input.iso_codes)
        self.assertListEqual(expected_exclude_languages, wikipedia_spider_input.exclude_iso_codes)
        self.assertEqual(EXPECTED_PAGE_SIZE, wikipedia_spider_input.page_size)
        self.assertEqual(expected_offset, wikipedia_spider_input.offset)
        self.assertEqual(EXPECTED_MAX_RECORDS, wikipedia_spider_input.max_records)

    def test_translated_site(self):
        translated_site_spider_input = SpiderInputFactory.get_spider_input(BBC_KEY, self.configs)
        self.assertIsInstance(translated_site_spider_input, TranslatedSiteSpiderInput)
        self.assertEqual(BBC_URL, translated_site_spider_input.url)
        self.assertEqual(BBC_SELECTOR, translated_site_spider_input.selector)

    def test_unknown_site(self):
        site = 'New York Times'
        with self.assertRaisesRegex(Exception, f'No spider configured for site {site}'):
            SpiderInputFactory.get_spider_input(site, self.configs)
