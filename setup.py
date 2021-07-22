from setuptools import setup

setup(
    name='language-indexing',
    version='0.0.1',
    url='https://github.com/wikitongues/Language-Indexing',
    author='Wikitongues',
    packages=[
        '',
        'config',
        'spiders',
        'data_store',
        'data_store.airtable'
    ],
    package_dir={
        '': 'wikitongues/wikitongues'
    },
    entry_points={
        'console_scripts': ['language-indexing=language_indexing:main']
    },
    install_requires=[
        'Scrapy'
    ],
    include_package_data=True
)
