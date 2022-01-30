import unittest

from wikitongues.wikitongues.lang_to_iso_converter import LangToIsoConverter


class TestLangToIsoConverter(unittest.TestCase):
    def setUp(self):
        self.lang_to_iso_converter = LangToIsoConverter()

    def test_get_iso_code(self):
        tests = [
            ("en-US", "eng"),
            ("fr", "fra"),
            ("xyzzy-Zorp!", None),
            ("fr-Brai", "fra"),
            ("ru-Cyrl-BY", "rus"),
            ("auto", None),
            ("", None),
        ]

        for test in tests:
            input = test[0]
            expected = test[1]
            actual = self.lang_to_iso_converter.get_iso_code(input)
            self.assertEqual(expected, actual)
