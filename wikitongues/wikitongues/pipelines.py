# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem

import logging


class WikitonguesPipeline:
    """
    Pipeline for checking for duplicates and adding new resources
    """

    def __init__(self, item_data_store):
        """
        Construct WikitonguesPipeline

        Args:
            item_data_store (ItemDataStore): Item data store instance
        """

        self.logger = logging.getLogger('pipelines.WikitonguesPipeline')
        self.item_data_store = item_data_store

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

        return cls(crawler.settings.get('ITEM_DATA_STORE'))

    def process_item(self, item, spider):
        """
        Called by the Scrapy framework for each item found by the spiders

        Args:
            item (scrapy.Item): The scraped item
            spider (Spider): The spider which scraped the item

        Raises:
            DropItem: Raised if the item is a duplicate of another item with \
the same url, associated with the same language

        Returns:
            scrapy.Item: The scraped item
        """

        url = item['url']
        iso_code = item['iso_code']
        result = self.item_data_store.get_item(url, iso_code)

        if result.data is not None:
            raise DropItem(
                f'Resource already indexed for language {iso_code}: {url}')

        self.item_data_store.create_item(item)

        return item
