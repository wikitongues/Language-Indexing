from wikitongues.wikitongues.data_store.airtable.airtable_item_formatter import AirtableItemFormatter  # noqa: E501

from wikitongues.wikitongues.items import WikitonguesItem

import unittest

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

        self.assertEqual(EXPECTED_ITEM['title'], result['Title'])
        self.assertEqual(EXPECTED_ITEM['url'], result['Coverage [Web]'])
        self.assertEqual(1, len(result['Subject [Language]']))
        self.assertEqual(EXPECTED_ITEM['language_id'],
                         result['Subject [Language]'][0])
