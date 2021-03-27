import scrapy

from items import WikitonguesItem


# Finds all the external links in the Wikipedia pages for the given languages
class WikipediaSpider(scrapy.Spider):
    # Used to identify the spider within the program
    name = "wikipedia"

    # Construct spider with arguments
    # languages: list of Language objects
    def __init__(self, languages, *args, **kwargs):
        super(WikipediaSpider, self).__init__(*args, **kwargs)
        self.languages = languages

    # Called once; starts initial HTTP requests to each requested Wikipedia
    # page
    def start_requests(self):
        def callback(language):
            return lambda response: self.parse_wikipedia_page(
                response, language)

        for language in self.languages:
            yield scrapy.Request(
                url=language.wikipedia_url,
                callback=callback(language))

    # Callback for HTTP response for Wikipedia pages. Locates external links
    # and makes HTTP requests
    def parse_wikipedia_page(self, response, language):
        links = response.css('a.external.text::attr(href)').getall()

        for link in links:
            yield scrapy.Request(
                link,
                lambda response: self.parse_external_link(response, language))

    # Callback for HTTP response for external links. If the response is good,
    # the link is indexed as a WikitonguesItem.
    def parse_external_link(self, response, language):
        if response.status != 200:
            pass

        yield WikitonguesItem(
            title=response.css('title::text').get(),
            url=response.url,
            iso_code=language.id,
            language_id=language.airtable_id,
            spider_name=self.name
        )
