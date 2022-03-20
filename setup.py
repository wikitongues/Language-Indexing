from setuptools import find_packages, setup

setup(
    name="language-indexing",
    version="0.0.1",
    url="https://github.com/wikitongues/Language-Indexing",
    author="Wikitongues",
    packages=find_packages(exclude=("test")),
    entry_points={"console_scripts": ["language-indexing=language_indexing.language_indexing:main"]},
    install_requires=["inflection", "languagecodes", "pre-commit", "requests", "responses", "Scrapy"],
    include_package_data=True,
)
