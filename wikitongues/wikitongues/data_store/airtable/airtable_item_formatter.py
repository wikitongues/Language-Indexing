from abc import ABC, abstractmethod
from .field_name import LINK_TEXT_FIELD, TITLE_FIELD, URL_FIELD, LANGUAGE_FIELD


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

        return {
            TITLE_FIELD: item['title'],
            URL_FIELD: item['url'],
            LINK_TEXT_FIELD: item['link_text'],
            LANGUAGE_FIELD: [
                item['language_id']
            ]
        }
