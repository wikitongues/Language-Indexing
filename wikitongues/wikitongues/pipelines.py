# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

import logging

from scrapy.exceptions import DropItem


class WikitonguesPipeline:
    """
    Pipeline for checking for duplicates and adding new resources
    """

    def __init__(self, external_resource_data_store):
        """
        Construct WikitonguesPipeline

        Args:
            external_resource_data_store (ExternalResourceDataStore): External resource data store instance
        """

        self.logger = logging.getLogger("pipelines.WikitonguesPipeline")
        self.external_resource_data_store = external_resource_data_store

    @classmethod
    def from_crawler(cls, crawler):
        """
                Called by the Scrapy framework. Instantiates a WikitonguesPipeline
        from the crawler settings

                Args:
                    crawler (Crawler): Crawler that uses this pipeline

                Returns:
                    WikitonguesPipeline: WikitonguesPipeline instance
        """

        return cls(crawler.settings.get("EXTERNAL_RESOURCE_DATA_STORE"))

    def process_item(self, item, spider):
        """
        Called by the Scrapy framework for each external resource

        Args:
            item (scrapy.Item): The scraped item
            spider (Spider): The spider which scraped the item

        Raises:
            DropItem: Raised if the item is a duplicate of another item with \
the same url, associated with the same language

        Returns:
            scrapy.Item: The scraped item
        """

        url = item.get("url")
        iso_code = item.get("iso_code", "")
        result = self.external_resource_data_store.get_external_resource(url, iso_code)

        if result.data is not None:
            if iso_code != "":
                raise DropItem(f"Resource already indexed for language {iso_code}: {url}")
            else:
                raise DropItem(f"Resource already indexed: {url}")

        create_result = self.external_resource_data_store.create_external_resource(item)

        if create_result.has_error():
            self.logger.error("\n".join(create_result.messages))

        return item
