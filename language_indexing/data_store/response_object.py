from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class ResponseObject(Generic[T]):
    """
    Response object containing the result of an operation and error \
information, if any
    """

    messages = []
    data = None

    def __init__(self):
        """
        Construct ResponseObject
        """

        self.messages: List[str] = []
        self.data: Optional[T] = None

    def add_message(self, message: str) -> None:
        """
        Add an error message to the response

        Args:
            message (str): Error message
        """

        self.messages.append(message)

    def has_error(self) -> bool:
        """
        Returns true if the response contains an error

        Returns:
            bool: True if there is an error
        """

        return len(self.messages) > 0
