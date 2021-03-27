from ..error_response import ErrorResponse

from ...language import Language

from abc import ABC, abstractmethod


class IAirtableLanguageExtractor(ABC):
    @abstractmethod
    def extract_languages_from_json(self, json_obj):
        pass

    @abstractmethod
    def extract_language_from_json(self, json_obj):
        pass


class AirtableLanguageExtractor(IAirtableLanguageExtractor):

    ID_PROPERTY = 'id'
    RECORDS = 'records'
    FIELDS = 'fields'
    IDENTIFIER = 'Identifier'
    STANDARD_NAME = 'Standardized Name'
    WIKIPEDIA_URL = 'wikipedia_url'

    def extract_languages_from_json(self, json_obj):
        result = ErrorResponse()

        records = json_obj.get(self.RECORDS)

        if type(records) != list:
            result.add_message(
                'Airtable API response missing list property \'records\'')
            return result

        languages = []
        for record in records:
            result1 = self.extract_language_from_json(record)

            if result1.has_error():
                return result1

            languages.append(result1.data)

        result.data = languages
        return result

    def extract_language_from_json(self, json_obj):
        result = ErrorResponse()

        fields = json_obj.get(self.FIELDS)

        if type(fields) != dict:
            result.add_message(
                'Airtable language record object missing object property '
                '\'fields\'')
            return result

        language_id = json_obj.get(self.ID_PROPERTY)

        if type(language_id) != str:
            result.add_message(
                'Airtable language record missing property \'id\'')
            return result

        result.data = Language(
            fields.get(self.IDENTIFIER),
            fields.get(self.STANDARD_NAME),
            fields.get(self.WIKIPEDIA_URL),
            language_id)

        return result
