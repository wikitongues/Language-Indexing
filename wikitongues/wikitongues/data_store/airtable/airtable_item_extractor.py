from ..error_response import ErrorResponse

from ...items import WikitonguesItem

from abc import ABC, abstractmethod

RECORDS = 'records'
FIELDS = 'fields'
TITLE_FIELD = 'Title'
URL_FIELD = 'Url'
ISO_FIELD = 'ISO Code'
LANGUAGE_FIELD = 'Language'
SPIDER_FIELD = 'Spider'


class IAirtableItemExtractor(ABC):
    @abstractmethod
    def extract_items_from_json(self, json_obj):
        pass

    @abstractmethod
    def extract_item_from_json(self, json_obj):
        pass


class AirtableItemExtractor(IAirtableItemExtractor):
    def extract_items_from_json(self, json_obj):
        result = ErrorResponse()

        records = json_obj.get(RECORDS)

        if type(records) != list:
            result.add_message(
                'Airtable API response missing list property \'records\'')
            return result

        items = []
        for record in records:
            result1 = self.extract_item_from_json(record)

            if result1.has_error():
                return result1

            items.append(result1.data)

        result.data = items
        return result

    def extract_item_from_json(self, json_obj):
        result = ErrorResponse()

        fields = json_obj.get(FIELDS)

        if type(fields) != dict:
            result.add_message(
                'Airtable item record object missing object property '
                '\'fields\'')
            return result

        result.data = WikitonguesItem(
            title=fields.get(TITLE_FIELD),
            url=fields.get(URL_FIELD),
            iso_code=fields.get(ISO_FIELD)[0],
            language_id=fields.get(LANGUAGE_FIELD)[0],
            spider_name=fields.get(SPIDER_FIELD)
        )
        return result
