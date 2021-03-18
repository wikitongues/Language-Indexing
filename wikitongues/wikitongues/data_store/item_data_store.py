from abc import ABC, abstractmethod


class ItemDataStore(ABC):

    @abstractmethod
    def get_item(self, url):
        pass

    @abstractmethod
    def create_item(self, item):
        pass

    @abstractmethod
    def update_item(self, item):
        pass
