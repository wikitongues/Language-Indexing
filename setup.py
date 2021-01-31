from setuptools import setup

setup(
    name='language-indexing',
    version='0.0.1',
    url='https://github.com/wikitongues/Language-Indexing',
    author='Wikitongues',
    packages=[
        '',
        'spiders'
    ],
    package_dir={
        '': 'wikitongues/wikitongues'
    },
    scripts=['wikitongues/wikitongues/language-indexing'],
    install_requires=[
        'Scrapy'
    ]
)
