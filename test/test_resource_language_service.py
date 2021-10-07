from wikitongues.wikitongues.data_store.language_data_store import LanguageDataStore
from wikitongues.wikitongues.data_store.error_response import ErrorResponse
from wikitongues.wikitongues.lang_to_iso_converter import ILangToIsoConverter
from wikitongues.wikitongues.language import Language
from wikitongues.wikitongues.resource_language_service import ResourceLanguageService

import unittest

EXPECTED_LANG_1 = 'en-US'
EXPECTED_LANG_2 = 'en-GB'
EXPECTED_LANG_3 = 'de'
EXPECTED_LANG_4 = ''
EXPECTED_LANG_5 = 'zzz'
EXPECTED_ISO_1 = 'eng'
EXPECTED_ISO_2 = 'deu'
EXPECTED_ISO_3 = 'zzz'
EXPECTED_ID_1 = 'id1'
EXPECTED_ID_2 = 'id2'


class MockLangToIsoConverter(ILangToIsoConverter):
    def get_iso_code(self, lang_attribute):
        return {
            EXPECTED_LANG_1: EXPECTED_ISO_1,
            EXPECTED_LANG_2: EXPECTED_ISO_1,
            EXPECTED_LANG_3: EXPECTED_ISO_2,
            EXPECTED_LANG_4: None,
            EXPECTED_LANG_5: EXPECTED_ISO_3
        }[lang_attribute]


class MockLanguageDataStore(LanguageDataStore):
    def get_language(self, iso_code):
        mapping = {
            EXPECTED_ISO_1: EXPECTED_ID_1,
            EXPECTED_ISO_2: EXPECTED_ID_2
        }
        result = ErrorResponse()
        if iso_code not in mapping:
            language = None
        else:
            language = Language(iso_code, '', '', mapping[iso_code])
        result.data = language
        return result

    def get_languages(self, iso_codes):
        pass

    def list_languages(self, page_size, offset, max_records):
        pass


class TestResourceLanguageService(unittest.TestCase):
    def setUp(self):
        language_data_store = MockLanguageDataStore()
        lang_to_iso_converter = MockLangToIsoConverter()
        self.resource_language_service = ResourceLanguageService(language_data_store, lang_to_iso_converter)

    def test_get_resource_language_ids(self):
        result = self.resource_language_service.get_resource_language_ids({
            EXPECTED_LANG_1,
            EXPECTED_LANG_2,
            EXPECTED_LANG_3,
            EXPECTED_LANG_4,
            EXPECTED_LANG_5
        })

        self.assertEqual(2, len(result))
        self.assertIn(EXPECTED_ID_1, result)
        self.assertIn(EXPECTED_ID_2, result)
