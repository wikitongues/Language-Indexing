import json
import unittest

from wikitongues.wikitongues.data_store.airtable.airtable_language_extractor import (
    AirtableLanguageExtractor,
)


class TestAirtableLanguageExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = AirtableLanguageExtractor()

    def test_extract_languages(self):
        with open("test/resources/languages.json") as f:
            json_obj = json.load(f)

        result = self.extractor.extract_languages_from_json(json_obj)

        self.assertFalse(result.has_error())

        data = result.data

        self.assertEqual(len(data), 3)

        self.assertEqual(data[0].id, "aaa")
        self.assertEqual(data[0].standard_name, "Ghotuo")
        self.assertEqual(data[0].wikipedia_url, "https://en.wikipedia.org/wiki/Ghotuo_language")

        self.assertEqual(data[1].id, "aab")
        self.assertEqual(data[1].standard_name, "Alumu-Tesu")
        self.assertEqual(data[1].wikipedia_url, "https://en.wikipedia.org/wiki/Alumu_language")

        self.assertEqual(data[2].id, "aac")
        self.assertEqual(data[2].standard_name, "Ari")
        self.assertEqual(
            data[2].wikipedia_url,
            "https://en.wikipedia.org/wiki/Ari_language_(New_Guinea)",
        )

    def test_extract_empty_list(self):
        with open("test/resources/emptyRecords.json") as f:
            json_obj = json.load(f)

        result = self.extractor.extract_languages_from_json(json_obj)

        self.assertFalse(result.has_error())

        self.assertEqual(len(result.data), 0)

    def test_extract_bad_json(self):
        json_obj = {}

        result = self.extractor.extract_languages_from_json(json_obj)

        self.assertTrue(result.has_error())
        self.assertEqual(result.messages[0], "Airtable API response missing list property 'records'")

    def test_extract_bad_records(self):
        json_obj = {"records": ""}
        result = self.extractor.extract_languages_from_json(json_obj)

        self.assertTrue(result.has_error())
        self.assertEqual(result.messages[0], "Airtable API response missing list property 'records'")

    def test_extract_bad_record(self):
        json_obj = {"records": [{}]}
        result = self.extractor.extract_languages_from_json(json_obj)

        self.assertTrue(result.has_error())
        self.assertEqual(
            result.messages[0],
            "Airtable language record object missing object property " "'fields'",
        )

    def test_extract_bad_fields(self):
        json_obj = {"records": [{"fields": ""}]}
        result = self.extractor.extract_languages_from_json(json_obj)

        self.assertTrue(result.has_error())
        self.assertEqual(
            result.messages[0],
            "Airtable language record object missing object property " "'fields'",
        )


if __name__ == "__main__":
    unittest.main()
