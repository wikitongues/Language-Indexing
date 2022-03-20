from types import SimpleNamespace

from scrapy.crawler import CrawlerProcess

# Under the hood, Scrapy doesn't support relative imports
# https://github.com/scrapy/scrapy/blob/9a28eb0bad1acf986d997905a410058f77911b7c/scrapy/utils/misc.py#L61
_PIPELINE_MODULE = "language_indexing.pipelines.WikitonguesPipeline"


class CrawlerProcessFactory:
    @staticmethod
    def get_crawler_process(configs: SimpleNamespace) -> CrawlerProcess:
        return CrawlerProcess(
            settings={
                "FEEDS": {"items.jl": {"format": "jl"}},
                "EXTERNAL_RESOURCE_DATA_STORE": configs.external_resource_data_store,
                "ITEM_PIPELINES": {_PIPELINE_MODULE: 300},
                "METAREFRESH_IGNORE_TAGS": ["script", "noscript"],
            }
        )
