from types import SimpleNamespace

from scrapy.crawler import CrawlerProcess


class CrawlerProcessFactory:
    @staticmethod
    def get_crawler_process(configs: SimpleNamespace) -> CrawlerProcess:
        return CrawlerProcess(
            settings={
                "FEEDS": {
                    "items.jl": {
                        "format": "jl"
                    }
                },
                'EXTERNAL_RESOURCE_DATA_STORE': configs.external_resource_data_store,
                'ITEM_PIPELINES': {
                    'pipelines.WikitonguesPipeline': 300
                },
                'METAREFRESH_IGNORE_TAGS': ['script', 'noscript']
            }
        )
