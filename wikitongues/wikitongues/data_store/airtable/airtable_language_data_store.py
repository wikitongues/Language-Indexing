from wikitongues.data_store.language_data_store import LanguageDataStore

class AirtableLanguageDataStore(LanguageDataStore):

    def __init__(self, http_client, language_extractor):
        self._client = http_client
        self._extractor = language_extractor

    def get_language(self, iso_code):
        pass

    def get_languages(self, iso_codes):
        pass

    def list_languages(self):
        response = self._client.list_records()
        return self._extractor.extract_language_from_json(response.text)
