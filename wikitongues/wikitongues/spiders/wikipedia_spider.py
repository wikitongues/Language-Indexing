import scrapy

from items import WikitonguesItem


class WikipediaSpiderInput:
    iso_codes = []
    exclude_iso_codes = []

    def __init__(self, iso_codes, exclude_iso_codes, page_size,
                 offset, max_records):
        self.iso_codes = iso_codes
        self.exclude_iso_codes = exclude_iso_codes
        self.page_size = page_size
        self.offset = offset
        self.max_records = max_records


# Finds all the external links in the Wikipedia pages for the given languages
class WikipediaSpider(scrapy.Spider):
    # Used to identify the spider within the program
    name = "wikipedia"

    # Construct spider with arguments
    # spider_input: WikipediaSpiderInput object specifying input data
    #   for this crawl
    # language_data_store: LanguageDataStore instance
    def __init__(self, spider_input, language_data_store, *args, **kwargs):
        super(WikipediaSpider, self).__init__(*args, **kwargs)
        self._spider_input = spider_input
        self._language_data_store = language_data_store

    # Load Language objects to target in this crawl
    def load_languages(self):
        if self._spider_input.iso_codes is not None:
            result = self._language_data_store.get_languages(
                self._spider_input.iso_codes)

            if result.has_error():
                return []

            return result.data

        elif self._spider_input.exclude_iso_codes is not None:
            result = filter(lambda x: x not in
                            self._spider_input.exclude_iso_codes,
                            self._language_data_store.list_languages(
                                self._spider_input.page_size,
                                self._spider_input.max_records,
                                offset=self._spider_input.offset).data)
            return list(result)

        else:
            result = self._language_data_store.list_languages(
                self._spider_input.page_size,
                self._spider_input.max_records,
                offset=self._spider_input.offset)
            return result.data

    # Called once; starts initial HTTP requests to each requested Wikipedia
    # page
    def start_requests(self):
        languages = self.load_languages()

        def callback(language):
            return lambda response: self.parse_wikipedia_page(
                response, language)

        for language in languages:
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
