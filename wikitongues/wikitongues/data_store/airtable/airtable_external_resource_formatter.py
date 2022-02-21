from abc import ABC, abstractmethod

from ...items import ExternalResource
from . import field_name


class IAirtableExternalResourceFormatter(ABC):
    """
    Airtable external resource formatter interface

    Args:
        ABC
    """

    @abstractmethod
    def get_fields_dict(self, external_resource: ExternalResource) -> dict:
        """
        Returns dictionary of Airtable fields for the given ExternalResource

        Args:
            external_resource (ExternalResource): ExternalResource object
        """
        pass


class AirtableExternalResourceFormatter(IAirtableExternalResourceFormatter):
    """
    Utility for getting Airtable field dictionary for uploading external resources via the API

    Args:
        IAirtableExternalResourceFormatter
    """

    def get_fields_dict(self, external_resource: ExternalResource) -> dict:
        """
        Returns dictionary of Airtable fields for the given ExternalResource

        Args:
            external_resource (ExternalResource): ExternalResource object

        Returns:
            dict: Dictionary of Airtable fields
        """

        fields = {
            field_name.TITLE_FIELD: external_resource["title"],
            field_name.URL_FIELD: external_resource["url"],
            field_name.LINK_TEXT_FIELD: external_resource["link_text"],
            field_name.SPIDER_FIELD: external_resource["spider_name"],
        }

        if "resource_languages_raw" in external_resource:
            fields[field_name.RESOURCE_LANGUAGES_RAW_FIELD] = ",".join(external_resource["resource_languages_raw"])

        if "resource_languages" in external_resource:
            fields[field_name.RESOURCE_LANGUAGES_LOOKUP_FIELD] = list(external_resource["resource_languages"])

        if "language_id" in external_resource and external_resource["language_id"] is not None:
            fields[field_name.LANGUAGE_FIELD] = [external_resource["language_id"]]

        return fields
