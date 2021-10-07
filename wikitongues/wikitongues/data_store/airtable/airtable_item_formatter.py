from abc import ABC, abstractmethod
from . import field_name


class IAirtableItemFormatter(ABC):
    """
    Airtable item formatter interface

    Args:
        ABC
    """

    @abstractmethod
    def get_fields_dict(self, item):
        """
        Returns dictionary of Airtable fields for the given WikitonguesItem

        Args:
            item (WikitonguesItem): WikitonguesItem object
        """
        pass


class AirtableItemFormatter(IAirtableItemFormatter):
    """
    Utility for getting Airtable field dictionary for uploading items via the \
API

    Args:
        IAirtableItemFormatter
    """

    def get_fields_dict(self, item):
        """
        Returns dictionary of Airtable fields for the given WikitonguesItem

        Args:
            item (WikitonguesItem): WikitonguesItem object

        Returns:
            dict: Dictionary of Airtable fields
        """

        fields = {
            field_name.TITLE_FIELD: item['title'],
            field_name.URL_FIELD: item['url'],
            field_name.LINK_TEXT_FIELD: item['link_text'],
            field_name.RESOURCE_LANGUAGES_RAW_FIELD: ','.join(item['resource_languages_raw']),
            field_name.RESOURCE_LANGUAGES_LOOKUP_FIELD: list(item['resource_languages'])
        }

        if 'language_id' in item:
            fields[field_name.LANGUAGE_FIELD] = [item['language_id']]

        return fields
