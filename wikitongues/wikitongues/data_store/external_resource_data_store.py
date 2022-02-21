from abc import ABC, abstractmethod

from ..items import ExternalResource
from .response_object import ResponseObject


class ExternalResourceDataStore(ABC):
    """
    Interface for a data store of external resources

    Args:
        ABC
    """

    @abstractmethod
    def get_external_resource(self, url: str, iso_code: str) -> ResponseObject[ExternalResource]:
        """
        Retrieve an external resource from the data store

        Args:
            url (str): Url of external resource
            iso_code (str): ISO code of associated language
        """
        pass

    @abstractmethod
    def create_external_resource(self, external_resource: ExternalResource) -> ResponseObject[None]:
        """
        Create an external resource in the data store

        Args:
            external_resource (ExternalResource): Resource to add to data store
        """
        pass
