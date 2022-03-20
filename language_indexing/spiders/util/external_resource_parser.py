from typing import Optional

from scrapy.http import HtmlResponse, Response

from ...items import ExternalResource
from ...lang_attribute_parser import LangAttributeParser
from ...language import Language
from ...resource_language_service import IResourceLanguageService

TITLE_SELECTOR = "title::text"


class ExternalResourceParser:
    @staticmethod
    def parse_external_link(
        response: Response,
        link_text: str,
        resource_language_service: IResourceLanguageService,
        spider_name: str,
        language: Optional[Language] = None,
    ) -> ExternalResource:
        if response.status != 200:
            return

        iso_code = language.id if language is not None else None
        language_id = language.airtable_id if language is not None else None

        if isinstance(response, HtmlResponse):
            lang_attrs = LangAttributeParser.get_lang_values(response)

            resource_language_ids = resource_language_service.get_resource_language_ids(lang_attrs)

            yield ExternalResource(
                title=response.css(TITLE_SELECTOR).get(),
                link_text=link_text,
                url=response.url,
                iso_code=iso_code,
                language_id=language_id,
                spider_name=spider_name,
                resource_languages=resource_language_ids,
                resource_languages_raw=lang_attrs,
            )

        else:
            yield ExternalResource(
                title=link_text,
                link_text=link_text,
                url=response.url,
                iso_code=iso_code,
                language_id=language_id,
                spider_name=spider_name,
            )
