from wikitongues.wikitongues.data_store.airtable.airtable_item_extractor import AirtableItemExtractor  # noqa: E501

import unittest
import json


class TestAirtableItemExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = AirtableItemExtractor()

    def test_extract_item(self):
        with open('test/resources/singleItem.json') as f:
            json_obj = json.load(f)

        result = self.extractor.extract_items_from_json(json_obj)

        self.assertFalse(result.has_error())

        data = result.data

        self.assertEqual(1, len(data))

        self.assertEqual(data[0]['title'], 'Wikitongues')
        self.assertEqual(data[0]['url'], 'wikitongues.org')
        self.assertEqual(data[0]['language_id'], 'recSlsrFcqniXRYy8')
        self.assertEqual(data[0]['iso_code'], 'aaa')

    def test_extract_empty_list(self):
        with open('test/resources/emptyRecords.json') as f:
            json_obj = json.load(f)

        result = self.extractor.extract_items_from_json(json_obj)

        self.assertFalse(result.has_error())

        self.assertEqual(len(result.data), 0)

    def test_extract_bad_json(self):
        json_obj = {}

        result = self.extractor.extract_items_from_json(json_obj)

        self.assertTrue(result.has_error())
        self.assertEqual(
            result.messages[0],
            'Airtable API response missing list property \'records\'')

    def test_extract_bad_records(self):
        json_obj = {
            'records': ''
        }
        result = self.extractor.extract_items_from_json(json_obj)

        self.assertTrue(result.has_error())
        self.assertEqual(
            result.messages[0],
            'Airtable API response missing list property \'records\'')

    def test_extract_bad_record(self):
        json_obj = {
            'records': [
                {}
            ]
        }
        result = self.extractor.extract_items_from_json(json_obj)

        self.assertTrue(result.has_error())
        self.assertEqual(
            result.messages[0],
            'Airtable item record object missing object property '
            '\'fields\'')

    def test_extract_bad_fields(self):
        json_obj = {
            'records': [
                {
                    'fields': ''
                }
            ]
        }
        result = self.extractor.extract_items_from_json(json_obj)

        self.assertTrue(result.has_error())
        self.assertEqual(
            result.messages[0],
            'Airtable item record object missing object property '
            '\'fields\'')
