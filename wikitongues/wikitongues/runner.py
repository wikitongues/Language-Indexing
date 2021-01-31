import scrapy
from scrapy.crawler import CrawlerProcess

from spiders.wikipedia_spider import WikipediaSpider

from language import Language

languages = [
    Language('sah', 'Sakha', 'https://en.wikipedia.org/wiki/Yakut_language'),
    Language('nrf', 'Jèrriais', 'https://en.wikipedia.org/wiki/J%C3%A8rriais'),
    Language('qwe', 'Quechua', 'https://en.wikipedia.org/wiki/Quechuan_languages'),
    Language('nys', 'Nyungar', 'https://en.wikipedia.org/wiki/Nyungar_language'),
    Language('xho', 'Xhosa', 'https://en.wikipedia.org/wiki/Xhosa_language'),
    Language('dak', 'Sioux', 'https://en.wikipedia.org/wiki/Sioux_language')
]

process = CrawlerProcess(
    settings={
        "FEEDS": {
            "items.jl": {
                "format": "jl"
            }
        }
    }
)

process.crawl(WikipediaSpider, languages)

process.start()