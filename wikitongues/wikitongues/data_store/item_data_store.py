from abc import ABC, abstractmethod


class ItemDataStore(ABC):

    @abstractmethod
    def get_item(self, url, iso_code):
        pass

    @abstractmethod
    def create_item(self, item):
        pass
