from spiders.wikipedia_spider import WikipediaSpiderInput
from spiders.translated_site_spider import TranslatedSiteSpiderInput
from config.load_configs import read_exclude_languages, read_include_languages
from data_store.airtable.offset_utility import OffsetUtility


class SpiderInputFactory:

    @staticmethod
    def get_spider_input(site, configs):
        if site == 'wikipedia':
            return WikipediaSpiderInput(
                read_include_languages(configs.main_config),
                read_exclude_languages(configs.main_config),
                configs.config_languages_table['page_size'],
                OffsetUtility.read_offset(),
                configs.config_languages_table['max_records']
            )
        elif site == 'translated_site':
            return TranslatedSiteSpiderInput(
                configs.main_config['translated_site']['url'],
                configs.main_config['translated_site']['selector']
            )

        raise Exception(f'Unrecognized site {site}')
