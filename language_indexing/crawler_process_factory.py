from types import SimpleNamespace

from scrapy.crawler import CrawlerProcess

from .config.load_configs import read_logging_settings
from .util.path_util import abspath

# Under the hood, Scrapy doesn't support relative imports
# https://github.com/scrapy/scrapy/blob/9a28eb0bad1acf986d997905a410058f77911b7c/scrapy/utils/misc.py#L61
_PIPELINE_MODULE = "language_indexing.pipelines.WikitonguesPipeline"


class CrawlerProcessFactory:
    @staticmethod
    def get_crawler_process(configs: SimpleNamespace) -> CrawlerProcess:
        logging_settings = read_logging_settings(configs.main_config)
        log_file = abspath(logging_settings.log_file)

        if log_file:
            print(f"Logging to {log_file}")

        return CrawlerProcess(
            settings={
                "FEEDS": {"items.jl": {"format": "jl"}},
                "EXTERNAL_RESOURCE_DATA_STORE": configs.external_resource_data_store,
                "ITEM_PIPELINES": {_PIPELINE_MODULE: 300},
                "LOG_FILE": log_file,
                "LOG_FILE_APPEND": logging_settings.log_file_append,
                "LOG_LEVEL": logging_settings.log_level,
                "METAREFRESH_IGNORE_TAGS": ["script", "noscript"],
            }
        )
