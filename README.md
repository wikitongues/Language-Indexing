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

## Install locally:
Clone the repository and run from the root directory:
```
pip install .
```

# Run
```
language-indexing
```

# Develop
This project utilizes [Scrapy](https://docs.scrapy.org/en/latest/intro/tutorial.html), a web crawling framework.

Using a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for development is recommended.

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
Run this after creating the virtual environment and after changing the code.
This installs the project and its dependencies into the active environment.
You'll be able to run the tool with the `language-indexing` command.
```
pip install .
```
## Run style guide check
Install [flake8](https://flake8.pycqa.org/en/latest/) if it is not already on your system.
Run from the root directory:
```
flake8
```
If you use Visual Studio Code, you can install these extensions to assist with following the style guide:
* cornflakes-linter: highlight flake8 style guide problems
* EditorConfig: Automatically fix whitespace problems

## Run unit tests
```
python -m unittest
```

# Contribute
We're looking for help developing this tool.
We invite contributors of any skill level.
Please contact [Scott](mailto:scott@wikitongues.org) if you are interested!
