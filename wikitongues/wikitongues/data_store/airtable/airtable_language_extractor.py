from abc import ABC, abstractmethod

from language import Language

from ..error_response import ErrorResponse


class IAirtableLanguageExtractor(ABC):
    """
    Airtable language extractor interface

    Args:
        ABC
    """

    @abstractmethod
    def extract_languages_from_json(self, json_obj):
        """
        Extract list of Language objects from Airtable API response JSON

        Args:
            json_obj (dict): Response from Airtable API
        """
        pass

    @abstractmethod
    def extract_language_from_json(self, json_obj):
        """
        Extract Language object from Airtable API response JSON

        Args:
            json_obj (dict): Response from Airtable API
        """
        pass


class AirtableLanguageExtractor(IAirtableLanguageExtractor):
    """
    Utility for extracting Language objects from Airtable API response JSON

    Args:
        IAirtableLanguageExtractor
    """

    ID_PROPERTY = "id"
    RECORDS = "records"
    FIELDS = "fields"
    IDENTIFIER = "Identifier"
    STANDARD_NAME = "Standardized Name"
    WIKIPEDIA_URL = "wikipedia_url"

    def extract_languages_from_json(self, json_obj):
        """
        Extract list of Language objects from Airtable API response JSON

        Args:
            json_obj (dict): Response from Airtable API

        Returns:
            ErrorResponse: Response object containing list of Language objects
        """

        result = ErrorResponse()

        records = json_obj.get(self.RECORDS)

        if type(records) != list:
            result.add_message("Airtable API response missing list property 'records'")
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
        """
        Extract Language object from Airtable API response JSON

        Args:
            json_obj (dict): Response from Airtable API

        Returns:
            ErrorResponse: Response object containing Language object
        """

        result = ErrorResponse()

        fields = json_obj.get(self.FIELDS)

        if type(fields) != dict:
            result.add_message("Airtable language record object missing object property " "'fields'")
            return result

        language_id = json_obj.get(self.ID_PROPERTY)

        if type(language_id) != str:
            result.add_message("Airtable language record missing property 'id'")
            return result

        result.data = Language(
            fields.get(self.IDENTIFIER),
            fields.get(self.STANDARD_NAME),
            fields.get(self.WIKIPEDIA_URL),
            language_id,
        )

        return result
