from setuptools import setup

setup(
    name="language-indexing",
    version="0.0.1",
    url="https://github.com/wikitongues/Language-Indexing",
    author="Wikitongues",
    packages=[
        "",
        "config",
        "spiders",
        "spiders.util",
        "data_store",
        "data_store.airtable",
    ],
    package_dir={"": "wikitongues/wikitongues"},
    entry_points={"console_scripts": ["language-indexing=language_indexing:main"]},
    install_requires=["inflection", "languagecodes", "requests", "responses", "Scrapy"],
    include_package_data=True,
)
