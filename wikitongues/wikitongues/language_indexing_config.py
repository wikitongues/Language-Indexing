import os

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
        load_config(config, "config/indexing.cfg")
    else:
        #When a user file in the same directory is passed, read that file
        default_config = open(os.path.join(os.path.dirname(__file__),
                                           default_config_file_name), "r")
        if default_config is None:
            print("file not found")
        readline(config, default_config)


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
    for x in config['DEFAULT'].__dict__:
        setattr(config['airtable_items_table'], x, config['DEFAULT'][x])
        setattr(config['airtable_languages_table'], x, config['DEFAULT'][x])
