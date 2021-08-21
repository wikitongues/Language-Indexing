import scrapy

from items import WikitonguesItem


class TranslatedSiteSpider(scrapy.Spider):
    name = "translated_site"

    url = 'https://www.bbc.com/ws/languages'

    selector = '#english_version .units-list>li>a'

    def start_requests(self):
        yield scrapy.Request(
            url=self.url,
            callback=self.parse_links)

    def parse_links(self, response):
        links = response.css(self.selector)

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
