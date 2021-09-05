import scrapy

from items import WikitonguesItem


class TranslatedSiteSpiderInput:
    def __init__(self, url, selector):
        self.url = url
        self.selector = selector


class TranslatedSiteSpider(scrapy.Spider):
    name = "translated_site"

    def __init__(self, spider_input, *args, **kwargs):
        super(TranslatedSiteSpider, self).__init__(*args, **kwargs)
        self._spider_input = spider_input

    def start_requests(self):
        yield scrapy.Request(
            url=self._spider_input.url,
            callback=self.parse_links)

    def parse_links(self, response):
        self.logger.debug(
            f'Finding links by selector {self._spider_input.selector}')

        links = response.css(self._spider_input.selector)

        self.logger.debug(f'Found {len(links)} links')

        def callback(link_text):
            return lambda response: self.parse_linked_page(response, link_text)

        for link in links:
            yield scrapy.Request(
                url=link.attrib['href'],
                callback=callback(link.css('::text').get()))

    def parse_linked_page(self, response, link_text):
        if response.status != 200:
            pass

        yield WikitonguesItem(
            title=response.css('title::text').get(),
            link_text=link_text,
            url=response.url,
            spider_name=self.name
        )
