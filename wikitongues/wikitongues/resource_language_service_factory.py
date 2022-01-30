from types import SimpleNamespace

from lang_to_iso_converter import LangToIsoConverter
from resource_language_service import ResourceLanguageService


class ResourceLanguageServiceFactory:
    @staticmethod
    def get_resource_language_service(
        configs: SimpleNamespace,
    ) -> ResourceLanguageService:
        language_data_store = configs.language_data_store
        lang_to_iso_converter = LangToIsoConverter()
        return ResourceLanguageService(language_data_store, lang_to_iso_converter)
