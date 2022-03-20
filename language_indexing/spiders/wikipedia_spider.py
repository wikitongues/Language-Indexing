import scrapy

from ..data_store.language_data_store import LanguageDataStore
from ..resource_language_service import IResourceLanguageService
from .input.wikipedia_spider_input import WikipediaSpiderInput
from .util.targeted_spider_util import TargetedSpiderUtil
from .util.wikipedia_util import WikipediaUtil


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
        spider_input: WikipediaSpiderInput,
        language_data_store: LanguageDataStore,
        resource_language_service: IResourceLanguageService,
        *args,
        **kwargs,
    ) -> None:
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
                response, language, self._resource_language_service, self.name
            )

        for language in languages:
            yield scrapy.Request(url=language.wikipedia_url, callback=callback(language))
