class ErrorResponse:
    """
    Response object containing the result of an operation and error \
information, if any
    """

    messages = []
    data = None

    def __init__(self):
        """
        Construct ErrorResponse
        """

        self.messages = []
        self.data = None

    def add_message(self, message):
        """
        Add an error message to the response

        Args:
            message (str): Error message
        """

        self.messages.append(message)

    def has_error(self):
        """
        Returns true if the response contains an error

        Returns:
            bool: True if there is an error
        """

        return len(self.messages) > 0
