import scrapy


from .util.targeted_spider_util import TargetedSpiderUtil
from .util.wikipedia_util import WikipediaUtil


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

    # Called once; starts initial HTTP requests to each requested Wikipedia
    # page
    def start_requests(self):
        languages = TargetedSpiderUtil.load_languages(self._spider_input, self._language_data_store)

        def callback(language):
            return lambda response: WikipediaUtil.parse_wikipedia_page(
                response,
                language,
                self._resource_language_service,
                self.name
            )

        for language in languages:
            yield scrapy.Request(
                url=language.wikipedia_url,
                callback=callback(language))
