import unittest
from unittest import mock

from language_indexing.util.path_util import abspath

MODULE_UNDER_TEST = "language_indexing.util.path_util"


class TestPathUtil(unittest.TestCase):
    @mock.patch(f"{MODULE_UNDER_TEST}.os.path.expanduser")
    def test_abspath(self, mock_expanduser):
        path = "~"
        expected_abspath = "/Users/me"
        mock_expanduser.return_value = expected_abspath
        result = abspath(path)
        self.assertEqual(result, expected_abspath)
        mock_expanduser.assert_called_once_with(path)

    def test_abspath_none(self):
        result = abspath(None)
        self.assertIsNone(result)
