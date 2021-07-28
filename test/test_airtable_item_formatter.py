from wikitongues.wikitongues.data_store.airtable.airtable_item_formatter import AirtableItemFormatter  # noqa: E501

from wikitongues.wikitongues.items import WikitonguesItem

import unittest
from wikitongues.wikitongues.data_store.airtable.field_name \
    import TITLE_FIELD, URL_FIELD, LANGUAGE_FIELD

EXPECTED_ITEM = WikitonguesItem(
    title='Title',
    url='aaa.com',
    iso_code='aaa',
    language_id='rec12345',
    spider_name='test'
)


class TestAirtableItemFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = AirtableItemFormatter()

    def test_get_fields_dict(self):
        result = self.formatter.get_fields_dict(EXPECTED_ITEM)

        self.assertEqual(EXPECTED_ITEM['title'], result[TITLE_FIELD])
        self.assertEqual(EXPECTED_ITEM['url'], result[URL_FIELD])
        self.assertEqual(1, len(result[LANGUAGE_FIELD]))
        self.assertEqual(EXPECTED_ITEM['language_id'],
                         result[LANGUAGE_FIELD][0])
