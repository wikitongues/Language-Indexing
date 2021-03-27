class AirtableItemIdProvider:
    def get_item_id(self, url, iso_code):
        return f'{iso_code}:{url}'
