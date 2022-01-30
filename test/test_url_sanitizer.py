import unittest

from wikitongues.wikitongues.url_sanitizer import UrlSanitizer


class TestUrlSanitizer(unittest.TestCase):
    def test_valid_url(self):
        urls = ["https://wikitongues.org/", "wikitongues.org", "www.wikitongues.org"]
        for url in urls:
            sanitized_url = UrlSanitizer.sanitize_url(url)
            self.assertEqual(url, sanitized_url)

    def test_url_missing_schema(self):
        url = "//wikitongues.org/"
        expected = "http://wikitongues.org/"
        sanitized_url = UrlSanitizer.sanitize_url(url)
        self.assertEqual(expected, sanitized_url)
