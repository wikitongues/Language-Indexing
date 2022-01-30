LANG_XPATH = "//@lang"


class LangAttributeParser:
    """
    Utility for parsing the unique lang attribute values from Scrapy response
    HTML
    """

    @staticmethod
    def get_lang_values(response):
        """
        Return a set of the unique lang attribute values

        Args:
            response (scrapy.http.response.html.HtmlResponse): Scrapy response
            object for HTML document

        Returns:
            set: Unique lang attribute values
        """
        lang_values = set(response.xpath(LANG_XPATH).getall())

        if "" in lang_values:
            lang_values.remove("")

        return lang_values
