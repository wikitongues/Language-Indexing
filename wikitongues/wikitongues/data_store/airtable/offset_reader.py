import os


class OffsetReader:
    """
    OffsetReader object contains offset value from file.
    """

    def __init__(self):
        """
        Construct OffsetReader
        """
        self.offset = None

    def read_offset(self):
        """
        Reads offset value from file

        Returns:
            offset (str): offset value
        """
        if os.path.exists(os.path.expanduser('~/.language-indexing-offset')):
            file = open(os.path.expanduser('~/.language-indexing-offset'), 'r')
            self.offset = file.read()
        return self.offset
