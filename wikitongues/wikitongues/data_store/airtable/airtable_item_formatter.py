from abc import ABC, abstractmethod


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
            'Title': item['title'],
            'Coverage [Web]': item['url'],
            'Subject [Language]': [
                item['language_id']
            ]
        }
