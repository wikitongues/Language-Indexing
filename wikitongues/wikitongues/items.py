# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikitonguesItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    language_id = scrapy.Field()
    spider_name = scrapy.Field()
