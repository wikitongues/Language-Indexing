class Language:
    """
    The Language class is (part of) the input to the program.
    It contains details used to locate web resources about a language.
    More fields will be added as we go.
    """

    def __init__(self, iso_code, standard_name, wikipedia_url, airtable_id=None):
        """
        Construct a Language object

        Args:
            iso_code (str): ISO code of the language - unique to each language
            standard_name (str): "Standard" name of the language
            wikipedia_url (str): URL of the language's Wikipedia page
            airtable_id (str, optional): ID of language assigned by Airtable
        """
        self.id = iso_code
        self.standard_name = standard_name
        self.wikipedia_url = wikipedia_url
        self.airtable_id = airtable_id
