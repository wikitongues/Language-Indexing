from wikitongues.wikitongues.data_store.airtable.airtable_item_formatter import AirtableItemFormatter  # noqa: E501

from wikitongues.wikitongues.items import WikitonguesItem

import unittest
from wikitongues.wikitongues.data_store.airtable.field_name \
    import LINK_TEXT_FIELD, TITLE_FIELD, URL_FIELD, LANGUAGE_FIELD

EXPECTED_ITEM = WikitonguesItem(
    title='Title',
    url='aaa.com',
    link_text='aaa link',
    iso_code='aaa',
    language_id='rec12345',
    spider_name='test'
)

EXPECTED_ITEM_WITHOUT_LANGUAGE = WikitonguesItem(
    title='Labaran Duniya - BBC News Hausa',
    url='https://www.bbc.com/hausa',
    link_text='Hausa',
    spider_name='test'
)


class TestAirtableItemFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = AirtableItemFormatter()

    def test_get_fields_dict(self):
        result = self.formatter.get_fields_dict(EXPECTED_ITEM)

        self.assertEqual(EXPECTED_ITEM['title'], result[TITLE_FIELD])
        self.assertEqual(EXPECTED_ITEM['url'], result[URL_FIELD])
        self.assertEqual(EXPECTED_ITEM['link_text'], result[LINK_TEXT_FIELD])
        self.assertEqual(1, len(result[LANGUAGE_FIELD]))
        self.assertEqual(EXPECTED_ITEM['language_id'],
                         result[LANGUAGE_FIELD][0])

    def test_get_fields_without_language(self):
        result = self.formatter.get_fields_dict(EXPECTED_ITEM_WITHOUT_LANGUAGE)

        self.assertEqual(
            EXPECTED_ITEM_WITHOUT_LANGUAGE['title'], result[TITLE_FIELD])
        self.assertEqual(
            EXPECTED_ITEM_WITHOUT_LANGUAGE['url'], result[URL_FIELD])
        self.assertEqual(
            EXPECTED_ITEM_WITHOUT_LANGUAGE['link_text'],
            result[LINK_TEXT_FIELD])
