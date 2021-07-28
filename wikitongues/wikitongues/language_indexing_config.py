import os
from sys import platform


class LanguageIndexingConfiguration:
    def __getitem__(self, key):
        return getattr(self, key)


# Save each section of the config as a object
class Title:
    def __getitem__(self, key):
        return getattr(self, key)


# Read in default properties
def load_config(config, default_config_file_name=None):

    #Default case: when nothing is passed, program reads the default config
    if default_config_file_name is None:
        config_file = open(os.path.join(os.path.dirname(__file__),
                                        "config/indexing.cfg"), "r")
    else:
        config_file = open(user_config_file())
    readline(config, config_file)


def user_config_file():
    if platform == "windows" or platform == "win32":
        env = os.getenv("APPDATA")
    elif platform == "linux" or platform == "linux2" or platform == "darwin":
        env = os.getenv("HOME")
    else:
        raise Exception("This program is intended only for Mac,"
                        + "Linux, or Windows machines.")
    return os.sep.join([env, 'wikitongues-language-indexing.cfg'])


def readline(config, default_config):
    title = Title()
    name = None
    for line in default_config:
        # Do nothing if it is a comment or empty line
        if line.startswith("#") or line.startswith('\n'):
            continue
        # Save the name for the section
        elif line.startswith("["):
            # When reach a new section, save everything before it into config
            if name is not None:
                setattr(config, name, title)
            name = line[1: -2]
            title = Title()
        # Save each individual data under the section
        else:
            word = line.split(" : ")
            # If there is no value for the key
            if len(word) == 1:
                setattr(title, word[0].rstrip(), None)
            # If there is value for the key
            else:
                setattr(title, word[0], word[1].rstrip())
    setattr(config, name, title)
    default_config.close()
    setDefault(config)


def setDefault(config):
    for value in config['DEFAULT'].__dict__:
        setattr(config['airtable_items_table'],
                value,
                config['DEFAULT'][value])
        setattr(config['airtable_languages_table'],
                value,
                config['DEFAULT'][value])
