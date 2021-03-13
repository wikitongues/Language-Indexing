from wikitongues.wikitongues.data_store.airtable.airtable_language_extractor import AirtableLanguageExtractor  # noqa: E501

import unittest
import json


class TestAirtableLanguageExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = AirtableLanguageExtractor()

    def test_extract_languages(self):
        with open('test/resources/languages.json') as f:
            json_obj = json.load(f)

        result = self.extractor.extract_languages_from_json(json_obj)

        self.assertEqual(len(result), 3)

        self.assertEqual(result[0].id, 'aaa')
        self.assertEqual(result[0].standard_name, 'Ghotuo')
        self.assertEqual(
            result[0].wikipedia_url,
            'https://en.wikipedia.org/wiki/Ghotuo_language')

        self.assertEqual(result[1].id, 'aab')
        self.assertEqual(result[1].standard_name, 'Alumu-Tesu')
        self.assertEqual(
            result[1].wikipedia_url,
            'https://en.wikipedia.org/wiki/Alumu_language')

        self.assertEqual(result[2].id, 'aac')
        self.assertEqual(result[2].standard_name, 'Ari')
        self.assertEqual(
            result[2].wikipedia_url,
            'https://en.wikipedia.org/wiki/Ari_language_(New_Guinea)')

    def test_extract_empty_list(self):
        with open('test/resources/emptyRecords.json') as f:
            json_obj = json.load(f)

        result = self.extractor.extract_languages_from_json(json_obj)

        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
