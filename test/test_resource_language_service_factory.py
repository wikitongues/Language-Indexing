import unittest
from types import SimpleNamespace
from unittest import mock

from resource_language_service import ResourceLanguageService
from resource_language_service_factory import ResourceLanguageServiceFactory


class TestResourceLanguageServiceFactory(unittest.TestCase):
    def test_get_resource_language_service(self):
        configs = SimpleNamespace()
        configs.language_data_store = mock.Mock()

        resource_language_service = ResourceLanguageServiceFactory.get_resource_language_service(configs)

        self.assertIsInstance(resource_language_service, ResourceLanguageService)
