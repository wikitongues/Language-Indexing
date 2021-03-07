import scrapy

from items import WikitonguesItem

# Extracts links from a page containing an index of language resources


class CollectionSpider(scrapy.Spider):
    name = "collection"

    def __init__(self, languages, url, selector, *args, **kwargs):
        super(CollectionSpider, self).__init__(*args, **kwargs)
        self.languages = languages
        self.url = url
        self.selector = selector

    def start_requests(self):
        yield scrapy.Request(self.url, self.parse_index)

    def parse_index(self, response):
        links = response.css(f'{self.selector} a').getall()
        pass

    def parse_collection_item(self, response, language):
        if response.status != 200:
            pass

        yield WikitonguesItem(
            title=response.css('title::text').get(),
            url=response.url,
            language_id=language.id,
            spider_name=self.name
        )
