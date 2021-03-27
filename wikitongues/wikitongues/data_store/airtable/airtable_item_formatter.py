from abc import ABC, abstractmethod


class IAirtableItemFormatter(ABC):
    @abstractmethod
    def get_fields_dict(self, item):
        pass


class AirtableItemFormatter(IAirtableItemFormatter):

    def get_fields_dict(self, item):
        return {
            'Title': item['title'],
            'Url': item['url'],
            'Language': [
                item['language_id']
            ]
        }
