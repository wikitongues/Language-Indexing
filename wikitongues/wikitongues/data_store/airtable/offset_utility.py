import os

FILENAME = '~/.language-indexing-offset'


class OffsetUtility:
    """
    OffsetUtility class for reading and writing offset value.
    """

    @staticmethod
    def read_offset():
        """
        Reads offset value from file

        Returns:
            offset (str): offset value
        """
        offset = None
        if os.path.exists(os.path.expanduser(FILENAME)):
            file = open(os.path.expanduser(FILENAME, 'r'))
            offset = file.read()
        return offset

    @staticmethod
    def write_offset(offset):
        """
        Writes offset value to file.
        """
        if offset is not None:
            file = open(os.path.expanduser(FILENAME, 'w'))
            file.write(offset)
