class AirtableConnectionInfo:
    """Info required to connect to an Airtable base
    """
    def __init__(self, base_id, api_key):
        """Constructor

        Args:
            base_id (str): Base ID
            api_key (str): API key
        """
        self.base_id = base_id
        self.api_key = api_key
