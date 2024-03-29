from abc import ABC, abstractmethod
from typing import List

from ...items import ExternalResource
from ..response_object import ResponseObject
from .field_name import (
    FIELDS,
    ISO_FIELD,
    LANGUAGE_FIELD,
    LINK_TEXT_FIELD,
    RECORDS,
    SPIDER_FIELD,
    TITLE_FIELD,
    URL_FIELD,
)


class IAirtableExternalResourceExtractor(ABC):
    """
    Airtable external resource extractor interface

    Args:
        ABC
    """

    @abstractmethod
    def extract_external_resources_from_json(self, json_obj: dict) -> ResponseObject[List[ExternalResource]]:
        """
        Extracts a list of ExternalResource objects from Airtable API response JSON

        Args:
            json_obj (dict): Airtable API response object
        """
        pass

    @abstractmethod
    def extract_external_resource_from_json(self, json_obj: dict) -> ResponseObject[ExternalResource]:
        """
        Extracts a single ExternalResource object from Airtable API response JSON

        Args:
            json_obj (dict): Airtable API response object
        """
        pass


class AirtableExternalResourceExtractor(IAirtableExternalResourceExtractor):
    """
    Extracts ExternalResource objects from Airtable API response JSON

    Args:
        IAirtableExternalResourceExtractor
    """

    def extract_external_resources_from_json(self, json_obj: dict) -> ResponseObject[List[ExternalResource]]:
        """
        Extracts a list of ExternalResource objects from Airtable API response JSON

        Args:
            json_obj (dict): Airtable API response object

        Returns:
            ResponseObject: Response object containing list of ExternalResource objects
        """

        result = ResponseObject[List[ExternalResource]]()

        records = json_obj.get(RECORDS)

        if type(records) != list:
            result.add_message("Airtable API response missing list property 'records'")
            return result

        external_resources = []
        for record in records:
            result1 = self.extract_external_resource_from_json(record)

            if result1.has_error():
                return result1

            external_resources.append(result1.data)

        result.data = external_resources
        return result

    def extract_external_resource_from_json(self, json_obj: dict) -> ResponseObject[ExternalResource]:
        """
        Extracts a single ExternalResource object from Airtable API response JSON

        Args:
            json_obj (dict): Airtable API response object

        Returns:
            ResponseObject: Response object containing ExternalResource object
        """

        result = ResponseObject[ExternalResource]()

        fields = json_obj.get(FIELDS)

        if type(fields) != dict:
            result.add_message("Airtable external resource record object missing object property " "'fields'")
            return result

        result.data = ExternalResource(
            title=fields.get(TITLE_FIELD),
            url=fields.get(URL_FIELD),
            link_text=fields.get(LINK_TEXT_FIELD),
            iso_code=None if ISO_FIELD not in fields else fields.get(ISO_FIELD)[0],
            language_id=None if LANGUAGE_FIELD not in fields else fields.get(LANGUAGE_FIELD)[0],
            spider_name=fields.get(SPIDER_FIELD),
        )
        return result
