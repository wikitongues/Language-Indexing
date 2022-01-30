import json

from ..error_response import ErrorResponse
from ..external_resource_data_store import ExternalResourceDataStore
from . import field_name


class AirtableExternalResourceDataStore(ExternalResourceDataStore):
    """
    Performs actions on an Airtable base for external resources
    """

    def __init__(self, http_client, external_resource_extractor, external_resource_formatter):
        """
        Construct AirtableExternalResourceDataStore

        Args:
            http_client (IAirtableHttpClient): Airtable Http Client instance
            external_resource_extractor (IAirtableExternalResourceExtractor): External Resource Extractor instance
            external_resource_formatter (IAirtableExternalResourceFormatter): External Resource Formater instance
        """
        self._client = http_client
        self._extractor = external_resource_extractor
        self._formatter = external_resource_formatter

    def get_external_resource(self, url, iso_code):
        """
        Get external resource

        Args:
            url (str): Url of external resource
            iso_code (str): ISO code of associated language

        Returns:
            ErrorResponse: Response object with external resource
        """

        result = ErrorResponse()

        response = self._client.get_records_by_fields({field_name.URL_FIELD: url, field_name.ISO_FIELD: iso_code})

        json_obj = json.loads(response.text)
        extract_result = self._extractor.extract_external_resources_from_json(json_obj)

        if extract_result.has_error():
            return extract_result

        external_resources = extract_result.data

        if len(external_resources) == 0:
            return result

        result.data = external_resources[0]
        return result

    def create_external_resource(self, external_resource):
        """
        Create external resource in data store

        Args:
            external_resource (ExternalResource): ExternalResource object

        Returns:
            ErrorRespone: Response object
        """

        result = ErrorResponse()

        fields = self._formatter.get_fields_dict(external_resource)

        response = self._client.create_record(fields)

        if response.status_code != 200:
            result.add_message(
                "Airtable API request to create external resource returned status code " f"{response.status_code}"
            )
            result.add_message(response.text)
            return result

        return result
