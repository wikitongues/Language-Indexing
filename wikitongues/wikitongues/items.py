# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikitonguesItem(scrapy.Item):
    """
    WikitonguesItem is the output of the program.
    A WikitonguesItem is a web page to be indexed and stored.
    """

    # The title of the page, from the <title> tag
    title = scrapy.Field()

    # The url of the page
    url = scrapy.Field()

    # The ISO code of the associated language
    iso_code = scrapy.Field()

    # The Airtable identifier of the associated language
    language_id = scrapy.Field()

    # The spider that gathered the page
    spider_name = scrapy.Field()
