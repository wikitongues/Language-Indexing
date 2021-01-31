import scrapy

from items import WikitonguesItem

# Finds all the external links in the Wikipedia pages for the given languages


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"

    def __init__(self, languages, *args, **kwargs):
        super(WikipediaSpider, self).__init__(*args, **kwargs)
        self.languages = languages

    def start_requests(self):
        def callback(language):
            return lambda response: self.parse_wikipedia_page(
                response, language)

        for language in self.languages:
            yield scrapy.Request(
                url=language.wikipedia_url,
                callback=callback(language))

    def parse_wikipedia_page(self, response, language):
        links = response.css('a.external.text::attr(href)').getall()

        for link in links:
            yield scrapy.Request(
                link,
                lambda response: self.parse_external_link(response, language))

    def parse_external_link(self, response, language):
        if response.status != 200:
            pass

        yield WikitonguesItem(
            title=response.css('title::text').get(),
            url=response.url,
            language_id=language.id,
            spider_name=self.name
        )
