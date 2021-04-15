from abc import ABC, abstractmethod


class ItemDataStore(ABC):
    """
    Interface for a data store of crawled items

    Args:
        ABC
    """

    @abstractmethod
    def get_item(self, url, iso_code):
        """
        Retrieve an item from the data store

        Args:
            url (str): Url of item
            iso_code (str): ISO code of associated language
        """
        pass

    @abstractmethod
    def create_item(self, item):
        """
        Create an item in the data store

        Args:
            item (WikitonguesItem): Item to add to data store
        """
        pass
