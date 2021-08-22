from spiders.wikipedia_spider import WikipediaSpiderInput
from spiders.translated_site_spider import TranslatedSiteSpiderInput
from config.load_configs import read_exclude_languages, read_include_languages
from data_store.airtable.offset_utility import OffsetUtility


class SpiderInputFactory:

    @staticmethod
    def get_spider_input(site, configs):
        spider_for_site = configs.main_config['spiders'][site]

        if spider_for_site == 'WikipediaSpider':
            return WikipediaSpiderInput(
                read_include_languages(configs.main_config),
                read_exclude_languages(configs.main_config),
                configs.config_languages_table['page_size'],
                OffsetUtility.read_offset(),
                configs.config_languages_table['max_records']
            )

        elif spider_for_site == 'TranslatedSiteSpider':
            return TranslatedSiteSpiderInput(
                configs.main_config['translated_site_urls'][site],
                configs.main_config['translated_site_selectors'][site]
            )

        raise Exception(f'No spider configured for site {site}')
