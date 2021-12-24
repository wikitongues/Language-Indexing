from abc import ABC, abstractmethod


class ExternalResourceDataStore(ABC):
    """
    Interface for a data store of external resources

    Args:
        ABC
    """

    @abstractmethod
    def get_external_resource(self, url, iso_code):
        """
        Retrieve an external resource from the data store

        Args:
            url (str): Url of external resource
            iso_code (str): ISO code of associated language
        """
        pass

    @abstractmethod
    def create_external_resource(self, external_resource):
        """
        Create an external resource in the data store

        Args:
            external_resource (ExternalResource): Resource to add to data store
        """
        pass
