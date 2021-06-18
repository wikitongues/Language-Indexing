import sys
import os

# The LanguageIndexingConfiguration class includes multiple objects separate by their section
# inside the .cfg file. If you want to access table name inside language table you can access it using
# config.airtable_languages_table.id_column
class LanguageIndexingConfiguration:
    pass

# Save each section of the config as a object
class Title:
    pass

# Read in default properties
def load_config(config, default_config_file_name):
    try:
        default_config = open(os.path.join(sys.path[0], default_config_file_name), "r")
        if (default_config == None):
            print("file not found")
        title = Title()
        name = None
        for line in default_config:
            # Do nothing if it is a comment or empty line
            if line.startswith("#") or line.startswith('\n'):
                continue
            # Save the name for the section
            elif line.startswith("["):
                # When reach a new section, save everything before it into config
                if name != None:
                    setattr(config, name, title)
                name = line[1: -2]
                title = Title()
            # Save each individual data under the section
            else:
                word = line.split(" : ")
                setattr(title, word[0], word[1].rstrip())

        setattr(config, name, title)


    except IOError:
        print("File does not exist.")
        sys.exit(1)

    default_config.close()

# Read in properties from user file, overriding defaults
# def load_config(config1, user_config_file_name):

# Instantiate configuration object
config = LanguageIndexingConfiguration()

load_config(config, "indexing.cfg")

#print(config.airtable_items_table.page_size)
