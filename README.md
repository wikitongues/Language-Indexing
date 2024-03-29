# Wikitongues Language Indexing
This is the web crawling tool that powers language indexing at [Wikitongues](https://wikitongues.org).
The tool works by visiting a number of online platforms and gathering links related to every language in the world.
Wikitongues will provide these links as a resource to anyone who wants to learn, study, or revitalize their language.

# Background
With nearly four billion people online, there has been an explosion of mother-tongue content in the form of memes, YouTube channels, public feeds on WhatsApp and Telegram, and other kinds of accessible media. In addition, there are two centuries of linguistic research gathering dust in university archives. How many of the world's 7,000 languages are already accessible online? With web crawling, we plan to find an answer.

Learn more about the project [here](https://wikitongues.org/projects/language-indexing/).

# Setup
## Prerequisites:
To run this tool, Python 3 must be installed on your system.

## Use a virtual environment:
Run this in the root directory to setup a virtual environment.
You'll only need to do this once.
This will create an env folder in the root directory which will contain the project dependencies as well as the python executable itself.
```
python -m venv env
```
## Activate virtual environment:
Run this in the root directory to activate the virtual environment.
Do this whenever you open the project in a new shell.
This makes the installed dependencies available.
The command line should indicate when "env" is active.
### Mac/Unix/Linux:
```
source env/bin/activate
```
### Windows:
```
env\Scripts\activate.bat
```
## Install in virtual environment
Run this after creating the virtual environment and any time you change the code.
This installs the project and its dependencies into the active environment.
You'll be able to run the tool with the `language-indexing` command.
```
pip install .
```
# Run
Make sure your virtual environment is active in your current shell (see
above), and run the tool with this simple command:
```
language-indexing
```
You will be promped for some configuration details when you run the command for
the first time.

## Configure Airtable settings

The program uses Airtable as a data repository. Airtable is a hybrid
spreadsheet/database cloud service that Wikitongues uses. Language data is fetched from a Languages table, and web resources are
uploaded to an External Resources table. If during development you choose not to connect to Airtable, a small sample set of language data will be provided.

### <a name="airtableAPI"></a> Find your Airtable API Key and Base ID

* Follow [these instructions](https://support.airtable.com/hc/en-us/articles/219046777-How-do-I-get-my-API-key-) to get your API key
  * Copy and paste the API key to a file or note on your computer
* You'll also need the Base ID, which is a string of characters representing the name of the Airtable Base
  * Log on to the [Airtable API web page](https://airtable.com/api) and click on the link for your Language Indexing base
  * Once the page is fully loaded there will be a line in the Introduction section saying "The ID of this base is", followed by green text starting with `app`
  * Copy and paste the Base ID to a file or note on your computer
* You will be promped for the "number of languages per query", which will apply if you are running Wikipedia crawling without providing specific languages (see [below](#configureWikipedia))

## Start Web Crawling

After configuring, you will be prompted to start the web crawling process. You will then be prompted to choose from the sites that have been configured.
Type in a site from the list, press enter, and the process will begin.

Data for the gathered items will be written to a file called items.jl.

# Configure

Configure the program by editing your user config file:
* Mac/Unix/Linux: **~/wikitongues-language-indexing.cfg**
* Windows: **%appdata%\wikitongues-language-indexing.cfg**

## Configure Airtable Settings

Language data is fetched from a Languages table, and web resources are
uploaded to an External Resources table. Access to these tables is configured in the
`[airtable_languages_table]` and `[airtable_external_resources_table]` sections
respectively. Common configuration properties can be set in the `[DEFAULT]`
section. Values in the table-specific sections will override values in
`[DEFAULT]`.

Configure these properties:

`api_key`: Airtable API key (see [above](#airtableAPI))

`base_id`: ID of the Airtable base (see [above](#airtableAPI))

`fake`: Set to true if you do not wish to access Airtable during development.
If a fake Languages table is used, a small sample set of languages will be
provided.

`page_size`: The number of languages to target in a single run. (Only
applicable to the Languages table.) An offset value is stored so that languages
will not be repeated in subsequent runs.

`table_name`: Table name.

`id_column`: Name of the column used as an identifier.


## <a name="configureWikipedia"></a> Configure Wikipedia Crawling

The program targets Wikipedia by visiting the article for a language and indexing each of the external links.

### Include/Exclude Language Lists

To specify languages to target, provide the [ISO 639-3 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-3_codes), separated by commas, in the `include_languages` section.
For example, the following configuration targets Sakha and Xhosa:
```ini
[include_languages]
include_languages : sah,xho
```

To target all languages except the ones specified (subject to the configured `page_size`), provide the ISO 639-3 codes, separated by commas, in the `exclude_languages` section.
For example, the following configuration excludes English and Spanish:
```ini
[exclude_languages]
exclude_languages : eng,spa
```

## Configure Translated Site Crawling

The program can also crawl a "translated site" containing an index of multilingual links, e.g. a news site with editions in multiple languages.
To configure a new site, follow these steps (example shown for [BBC News](https://www.bbc.com/ws/languages)):

1. Add the site name to the `[sites]` section
```ini
[sites]
BBC
```

2. In the `[spiders]` section, specify that the site will be crawled using the `TranslatedSiteSpider` workflow
```ini
[spiders]
BBC : TranslatedSiteSpider
```

3. Provide the url containing the site's language index in the `[translated_site_urls]` section
```ini
[translated_site_urls]
BBC : https://www.bbc.com/ws/languages
```

4. Provide the CSS selector common to each link in the site's language index. You can use your browser's dev tools to find the selector.
```ini
[translated_site_selectors]
BBC : #english_version .units-list>li>a
```

# Develop
This project utilizes [Scrapy](https://docs.scrapy.org/en/latest/intro/tutorial.html), a web crawling framework.

This repository uses [pre-commit](https://pre-commit.com/) hooks to keep the code consistently formatted and readable, making for a good development experience for everyone who contributes to the code. Install pre-commit in your local environment before making your first commit:
```
pre-commit install
```
When you run `git commit`, the following hooks will be run:
* [check-yaml](https://github.com/pre-commit/pre-commit-hooks#check-yaml)
* [end-of-file-fixer](https://github.com/pre-commit/pre-commit-hooks#end-of-file-fixer)
* [trailing-whitespace](https://github.com/pre-commit/pre-commit-hooks#trailing-whitespace)
* [black](https://github.com/psf/black) (code formatter)
* [isort](https://github.com/pycqa/isort) (sorts `import` statements)

If any of the hooks "fails", it will make formatting changes to the offending files and prevent the commit. Simply stage the additional changes and re-run your `git commit` command if this occurs.

If you use Visual Studio Code, you can install these helpful extensions to fix formatting as you code:
* cornflakes-linter: highlight flake8 style guide problems
* EditorConfig: Automatically fix whitespace problems
* Python Docstring Generator: Type `"""` to generate the docstring template for a class or function

## Run unit tests
```
python -m unittest
```
Visual Studio Code provides a UI for running the tests.

# Contribute
We're looking for help developing this tool.
We invite contributors of any skill level.
Please contact [Scott](mailto:scott@wikitongues.org) if you are interested!
