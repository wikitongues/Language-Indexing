import os


class OffsetUtility:
    """
    OffsetReader object contains offset value from file.
    """

    def __init__(self):
        """
        Construct OffsetReader
        """
        self.offset = None

    @staticmethod
    def read_offset():
        """
        Reads offset value from file

        Returns:
            offset (str): offset value
        """
        if os.path.exists(os.path.expanduser('~/.language-indexing-offset')):
            file = open(os.path.expanduser('~/.language-indexing-offset'), 'r')
            offset = file.read()
        return offset

    @staticmethod
    def write_offset(offset):
        """
        Writes offset value to file.
        """
        if offset is not None:
            file = open(os.path.expanduser('~/.language-indexing-offset'), 'w')
            file.write('offset')
