# Wikitongues Language Indexing
This is the web crawling tool that powers language indexing at Wikitongues.
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
## Copy config file to home directory:
The program reads certain settings from a configuration file. The program
looks for this file in your home directory on Mac or Linux, or your appdata
directory on Windows. To copy a properly formatted config file to the correct
place run this command:
### Mac/Unix/Linux:
```
cp wikitongues/wikitongues/config/indexing.cfg ~/wikitongues-language-indexing.cfg
```

### Windows:
```
copy wikitongues\wikitongues\config\indexing.cfg %appdata%\wikitongues-language-indexing.cfg
```

# Configure

Configure the program by editing your user config file:
* Mac/Unix/Linux: **~/wikitongues-language-indexing.cfg**
* Windows: **%appdata%\wikitongues-language-indexing.cfg**

## Configure Airtable settings

The program uses Airtable as a data repository. Airtable is a hybrid
spreadsheet/database cloud service that Wikitongues uses.

Language data is fetched from a Languages table, and web resources are
uploaded to an Items table. Access to these tables is configured in the
`[airtable_languages_table]` and `[airtable_items_table]` sections
respectively. Common configuration properties can be set in the `[DEFAULT]`
section. Values in the table-specific sections will override values in
`[DEFAULT]`.

Configure these properties:

`api_key`: Airtable API key (see below)

`base_id`: ID of the Airtable base (see below)

`fake`: Set to true if you do not wish to access Airtable during development.
If a fake Languages table is used, a small sample set of languages will be
provided.

`page_size`: The number of languages to target in a single run. (Only
applicable to the Languages table.) An offset value is stored so that languages
will not be repeated in subsequent runs.

`table_name`: Table name.

`id_column`: Name of the column used as an identifier.

### Find your Airtable API Key and Base ID

* Follow [these instructions](https://support.airtable.com/hc/en-us/articles/219046777-How-do-I-get-my-API-key-) to get your API key
  * Copy and paste the API key to a file or note on your computer
* You'll also need the Base ID, which is a string of characters representing the name of the Airtable Base
  * Log on to the [Airtable API web page](https://airtable.com/api) and click on the link for your Language Indexing base
  * Once the page is fully loaded there will be a line in the Introduction section saying "The ID of this base is", followed by green text starting with `app`
  * Copy and paste the Base ID to a file or note on your computer

# Run
Make sure your virtual environment is active in your current shell (see
above), and run the tool with this simple command:
```
language-indexing
```
Data for the gathered items will be written to a file called items.jl.

# Develop
This project utilizes [Scrapy](https://docs.scrapy.org/en/latest/intro/tutorial.html), a web crawling framework.

## Run style guide check
Install [flake8](https://flake8.pycqa.org/en/latest/) if it is not already on your system.
Run from the root directory:
```
flake8
```
If you use Visual Studio Code, you can install these extensions to assist with following the style guide:
* cornflakes-linter: highlight flake8 style guide problems
* EditorConfig: Automatically fix whitespace problems
* Python Docstring Generator: Type `"""` to generate the docstring template for a class or function

## Run unit tests
```
python -m unittest
```

# Contribute
We're looking for help developing this tool.
We invite contributors of any skill level.
Please contact [Scott](mailto:scott@wikitongues.org) if you are interested!
