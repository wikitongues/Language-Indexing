import logging

from items import ExternalResource

from ..error_response import ErrorResponse
from ..external_resource_data_store import ExternalResourceDataStore


class FakeExternalResourceDataStore(ExternalResourceDataStore):
    def __init__(self):
        self.logger = logging.getLogger("data_store.airtable.fake_external_resource_data_store")

    def get_external_resource(self, url, iso_code):
        result = ErrorResponse()

        if iso_code == "xho" and url == "xhosa.com":
            result.data = ExternalResource(
                title="Xhosa Resource",
                url="xhosa.com",
                language_id="xho",
                spider_name="test",
            )

        return result

    def create_external_resource(self, external_resource):
        title = external_resource["title"]
        self.logger.info(f'Creating external resource "{title}"')

        return ErrorResponse()
