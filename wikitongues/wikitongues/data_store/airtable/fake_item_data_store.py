from ..item_data_store import ItemDataStore
from ..error_response import ErrorResponse
from items import WikitonguesItem

import logging


class FakeItemDataStore(ItemDataStore):
    def __init__(self):
        self.logger = logging.getLogger(
            'data_store.airtable.fake_item_data_store')

    def get_item(self, url, iso_code):
        result = ErrorResponse()

        if iso_code == 'xho' and url == 'xhosa.com':
            result.data = WikitonguesItem(
                title='Xhosa Resource',
                url='xhosa.com',
                language_id='xho',
                spider_name='test'
            )

        return result

    def create_item(self, item):
        title = item['title']
        self.logger.info(f'Creating item "{title}"')

        return ErrorResponse()
