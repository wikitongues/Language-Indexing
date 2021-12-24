import scrapy
from scrapy.http import HtmlResponse

from items import WikitonguesItem
from lang_attribute_parser import LangAttributeParser
from url_sanitizer import UrlSanitizer


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
    def __init__(
        self,
        spider_input,
        language_data_store,
        resource_language_service,
        *args,
        **kwargs
    ):
        super(WikipediaSpider, self).__init__(*args, **kwargs)

        self._spider_input = spider_input
        self._language_data_store = language_data_store
        self._resource_language_service = resource_language_service

    # Load Language objects to target in this crawl
    def load_languages(self):
        if self._spider_input.iso_codes is not None:
            result = self._language_data_store.get_languages(
                self._spider_input.iso_codes)

            if result.has_error():
                return []

            return result.data

        elif self._spider_input.exclude_iso_codes is not None:
            result = filter(lambda language: language.id not in
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
        links = response.css('a.external.text')

        def callback(link_text):
            return lambda response: self.parse_external_link(
                response, language, link_text)

        for link in links:
            url = link.attrib['href']
            if self.should_follow_external_link(url):
                yield scrapy.Request(
                    url=UrlSanitizer.sanitize_url(url),
                    callback=callback(link.css('::text').get()))

    def should_follow_external_link(self, url):
        return 'wikipedia.org' not in url

    # Callback for HTTP response for external links. If the response is good,
    # the link is indexed as a WikitonguesItem.
    def parse_external_link(self, response, language, link_text):
        if response.status != 200:
            pass

        if isinstance(response, HtmlResponse):
            lang_attrs = LangAttributeParser.get_lang_values(response)

            resource_language_ids = self._resource_language_service.get_resource_language_ids(lang_attrs)

            yield WikitonguesItem(
                title=response.css('title::text').get(),
                link_text=link_text,
                url=response.url,
                iso_code=language.id,
                language_id=language.airtable_id,
                spider_name=self.name,
                resource_languages=resource_language_ids,
                resource_languages_raw=lang_attrs
            )

        else:
            yield WikitonguesItem(
                title=link_text,
                link_text=link_text,
                url=response.url,
                iso_code=language.id,
                language_id=language.airtable_id,
                spider_name=self.name
            )
