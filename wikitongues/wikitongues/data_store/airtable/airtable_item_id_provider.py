class AirtableItemIdProvider:
    """
    Utility for providing the Airtable identifier for an item
    """

    def get_item_id(self, url, iso_code):
        """
        Returns the Airtable identifier for the item with the given properties

        Args:
            url (str): Url of item
            iso_code (str): ISO code of associated language

        Returns:
            str: Airtable identifier of item
        """

        return f'{iso_code}:{url}'
