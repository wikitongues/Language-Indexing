import scrapy

from .util.external_resource_parser import ExternalResourceParser


class TranslatedSiteSpiderInput:
    def __init__(self, url, selector):
        self.url = url
        self.selector = selector


class TranslatedSiteSpider(scrapy.Spider):
    name = "translated_site"

    def __init__(self, spider_input, resource_language_service, *args, **kwargs):
        super(TranslatedSiteSpider, self).__init__(*args, **kwargs)
        self._spider_input = spider_input
        self._resource_language_service = resource_language_service

    def start_requests(self):
        yield scrapy.Request(url=self._spider_input.url, callback=self.parse_links)

    def parse_links(self, response):
        self.logger.debug(f"Finding links by selector {self._spider_input.selector}")

        links = response.css(self._spider_input.selector)

        self.logger.debug(f"Found {len(links)} links")

        def callback(link_text):
            return lambda response: ExternalResourceParser.parse_external_link(
                response, link_text, self._resource_language_service, self.name
            )

        for link in links:
            yield scrapy.Request(url=link.attrib["href"], callback=callback(link.css("::text").get()))
