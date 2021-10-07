from wikitongues.wikitongues.data_store.airtable.airtable_item_formatter import AirtableItemFormatter  # noqa: E501
import wikitongues.wikitongues.data_store.airtable.field_name as field_name

from wikitongues.wikitongues.items import WikitonguesItem

import unittest

EXPECTED_ITEM = WikitonguesItem(
    title='Title',
    url='aaa.com',
    link_text='aaa link',
    iso_code='aaa',
    language_id='rec12345',
    spider_name='test',
    resource_languages={'id1', 'id2'},
    resource_languages_raw={'aaa', 'en'}
)

EXPECTED_ITEM_WITHOUT_LANGUAGE = WikitonguesItem(
    title='Labaran Duniya - BBC News Hausa',
    url='https://www.bbc.com/hausa',
    link_text='Hausa',
    spider_name='test',
    resource_languages={'id2', 'id3'},
    resource_languages_raw={'en', 'ha'}
)


class TestAirtableItemFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = AirtableItemFormatter()

    def test_get_fields_dict(self):
        result = self.formatter.get_fields_dict(EXPECTED_ITEM)

        self.assertEqual(EXPECTED_ITEM['title'], result[field_name.TITLE_FIELD])
        self.assertEqual(EXPECTED_ITEM['url'], result[field_name.URL_FIELD])
        self.assertEqual(EXPECTED_ITEM['link_text'], result[field_name.LINK_TEXT_FIELD])
        self.assertEqual(1, len(result[field_name.LANGUAGE_FIELD]))
        self.assertEqual(EXPECTED_ITEM['language_id'],
                         result[field_name.LANGUAGE_FIELD][0])

        self.assertIsInstance(result[field_name.RESOURCE_LANGUAGES_LOOKUP_FIELD], list)
        for lang in EXPECTED_ITEM['resource_languages']:
            self.assertIn(lang, result[field_name.RESOURCE_LANGUAGES_LOOKUP_FIELD])

        self.assertIsInstance(result[field_name.RESOURCE_LANGUAGES_RAW_FIELD], str)
        for lang in EXPECTED_ITEM['resource_languages_raw']:
            self.assertIn(lang, result[field_name.RESOURCE_LANGUAGES_RAW_FIELD])

    def test_get_fields_without_language(self):
        result = self.formatter.get_fields_dict(EXPECTED_ITEM_WITHOUT_LANGUAGE)

        self.assertEqual(
            EXPECTED_ITEM_WITHOUT_LANGUAGE['title'], result[field_name.TITLE_FIELD])
        self.assertEqual(
            EXPECTED_ITEM_WITHOUT_LANGUAGE['url'], result[field_name.URL_FIELD])
        self.assertEqual(
            EXPECTED_ITEM_WITHOUT_LANGUAGE['link_text'],
            result[field_name.LINK_TEXT_FIELD])

        self.assertIsInstance(result[field_name.RESOURCE_LANGUAGES_LOOKUP_FIELD], list)
        for lang in EXPECTED_ITEM_WITHOUT_LANGUAGE['resource_languages']:
            self.assertIn(lang, result[field_name.RESOURCE_LANGUAGES_LOOKUP_FIELD])

        self.assertIsInstance(result[field_name.RESOURCE_LANGUAGES_RAW_FIELD], str)
        for lang in EXPECTED_ITEM_WITHOUT_LANGUAGE['resource_languages_raw']:
            self.assertIn(lang, result[field_name.RESOURCE_LANGUAGES_RAW_FIELD])
