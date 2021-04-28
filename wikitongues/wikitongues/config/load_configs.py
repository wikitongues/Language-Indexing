import sys
from sys import platform
import configparser
import os

def load_configs():
    print("loading")
    #default_config_text = pkg_resources.read_text(config_pkg, 'indexing.cfg')
    default_config = configparser.ConfigParser()
    default_config.read('indexing.cfg')

    user_config = configparser.ConfigParser()

    if platform == "win32":
        env = os.getenv('APPDATA')
        env += '\\Wikitongues\\Indexing-Project\\'
    elif (platform == "linux" or platform == "linux2"):
        env = os.getenv('HOME')
        env += '/Wikitongues/Indexing-Project/'

    try:
        user_config_file = open(env + 'wikitongues-language-indexingo.cfg')
        user_config.read_file(user_config_file)
        pass
    except FileNotFoundError:
        print("Error: User config file not found")
        sys.exit(1)
        pass
    finally:
        user_config_file.close()
    # user_config.read_file(env + 'wikitongues-language-indexing.cfg')
    defualt_sites = default_config.items('sites')
    user_sites = user_config.items('sites')
    if user_sites[0][1] != "replace_me":
        # override sites configuration
        return user_sites
    else:
        # nothing overridden. return the default config settings
        return defualt_sites
