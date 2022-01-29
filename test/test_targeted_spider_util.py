import unittest
from unittest import mock

from language import Language

from wikitongues.wikitongues.data_store.error_response import ErrorResponse
from wikitongues.wikitongues.data_store.language_data_store import LanguageDataStore
from wikitongues.wikitongues.spiders.util.targeted_spider_util import TargetedSpiderUtil
from wikitongues.wikitongues.spiders.wikipedia_spider import WikipediaSpiderInput

LANG1 = mock.Mock(Language, id='eng')
LANG2 = mock.Mock(Language, id='spa')
LANG3 = mock.Mock(Language, id='sah')
LANG4 = mock.Mock(Language, id='xho')

EXPECTED_ISO_CODES = ['eng', 'spa']
EXPECTED_INCLUDED_LANGUAGES = [LANG1, LANG2]
EXPECTED_LANGUAGES = [LANG1, LANG2, LANG3, LANG4]
EXPECTED_PAGE_SIZE = 4
EXPECTED_MAX_RECORDS = 100
EXPECTED_OFFSET = 'offset'

MODULE_UNDER_TEST = 'wikitongues.wikitongues.spiders.util.targeted_spider_util'


class TestTargetedSpiderUtil(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_language_data_store = mock.Mock(LanguageDataStore)

        def mock_get_languages(iso_codes):
            response = ErrorResponse()

            if iso_codes == EXPECTED_ISO_CODES:
                response.data = EXPECTED_INCLUDED_LANGUAGES

            return response

        def mock_list_languages(page_size, max_records, offset):
            response = ErrorResponse()

            if page_size == EXPECTED_PAGE_SIZE and max_records == EXPECTED_MAX_RECORDS and offset == EXPECTED_OFFSET:
                response.data = EXPECTED_LANGUAGES

            return response

        self.mock_language_data_store.get_languages.side_effect = mock_get_languages
        self.mock_language_data_store.list_languages.side_effect = mock_list_languages

    def test_load_included_languages(self):
        input = WikipediaSpiderInput(EXPECTED_ISO_CODES, None, None, None, None)

        languages = TargetedSpiderUtil.load_languages(input, self.mock_language_data_store)

        self.assertListEqual(EXPECTED_INCLUDED_LANGUAGES, languages)

    def test_load_all_languages_but_excluded(self):
        input = WikipediaSpiderInput(
            None, EXPECTED_ISO_CODES, EXPECTED_PAGE_SIZE, EXPECTED_OFFSET, EXPECTED_MAX_RECORDS
        )
        expected_languages_minus_excluded = [LANG3, LANG4]

        languages = TargetedSpiderUtil.load_languages(input, self.mock_language_data_store)

        self.assertListEqual(expected_languages_minus_excluded, languages)

    def test_load_all_languages(self):
        input = WikipediaSpiderInput(None, None, EXPECTED_PAGE_SIZE, EXPECTED_OFFSET, EXPECTED_MAX_RECORDS)

        languages = TargetedSpiderUtil.load_languages(input, self.mock_language_data_store)

        self.assertListEqual(EXPECTED_LANGUAGES, languages)
