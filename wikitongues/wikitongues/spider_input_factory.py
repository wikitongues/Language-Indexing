import config.config_keys as keys
from config.load_configs import read_exclude_languages, read_include_languages
from data_store.airtable.offset_utility import OffsetUtility
from spiders.translated_site_spider import TranslatedSiteSpiderInput
from spiders.wikipedia_spider import WikipediaSpiderInput

WIKIPEDIA_SPIDER = "WikipediaSpider"
TRANSLATED_SITE_SPIDER = "TranslatedSiteSpider"


class SpiderInputFactory:
    @staticmethod
    def get_spider_input(site, configs):
        spider_for_site = configs.main_config[keys.SPIDERS_SECTION][site]

        if spider_for_site == WIKIPEDIA_SPIDER:
            return WikipediaSpiderInput(
                read_include_languages(configs.main_config),
                read_exclude_languages(configs.main_config),
                configs.config_languages_table[keys.PAGE_SIZE_KEY],
                OffsetUtility.read_offset(),
                configs.config_languages_table[keys.MAX_RECORDS_KEY],
            )

        elif spider_for_site == TRANSLATED_SITE_SPIDER:
            urls_key = keys.TRANSLATED_SITE_URLS_SECTION
            selectors_key = keys.TRANSLATED_SITE_SELECTORS_SECTION
            return TranslatedSiteSpiderInput(
                configs.main_config[urls_key][site],
                configs.main_config[selectors_key][site],
            )

        raise Exception(f"No spider configured for site {site}")
