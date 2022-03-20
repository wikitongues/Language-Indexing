class UrlSanitizer:
    """
    Utility for sanitizing url's
    """

    @staticmethod
    def sanitize_url(url: str) -> str:
        """
        Sanitizes url for Scrapy request

        Args:
            url (str): url

        Returns:
            str: Sanitized url
        """

        if url[:2] == "//":
            return "http:" + url

        return url
