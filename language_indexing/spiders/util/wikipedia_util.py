from typing import Callable, Iterator

import scrapy
from scrapy.http import HtmlResponse

from ...items import ExternalResource
from ...language import Language
from ...resource_language_service import IResourceLanguageService
from ...url_sanitizer import UrlSanitizer
from .external_resource_parser import ExternalResourceParser

EXTERNAL_LINK_SELECTOR = "a.external.text"
LINK_TEXT_SELECTOR = "::text"


class WikipediaUtil:
    @staticmethod
    def parse_wikipedia_page(
        response: HtmlResponse,
        language: Language,
        resource_language_service: IResourceLanguageService,
        spider_name: str,
    ) -> Iterator[scrapy.Request]:
        links = response.css(EXTERNAL_LINK_SELECTOR)

        def callback(link_text: str) -> Callable[[HtmlResponse], ExternalResource]:
            return lambda response: ExternalResourceParser.parse_external_link(
                response,
                link_text,
                resource_language_service,
                spider_name,
                language=language,
            )

        for link in links:
            url = link.attrib["href"]
            if WikipediaUtil._should_follow_external_link(url):
                yield scrapy.Request(
                    url=UrlSanitizer.sanitize_url(url),
                    callback=callback(link.css(LINK_TEXT_SELECTOR).get()),
                )

    @staticmethod
    def _should_follow_external_link(url: str) -> bool:
        return "wikipedia.org" not in url
