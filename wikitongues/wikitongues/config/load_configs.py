import sys
from sys import platform
import configparser
import os

def load_configs():
    print("loading config file")
    #default_config_text = pkg_resources.read_text(config_pkg, 'indexing.cfg')
    default_config = configparser.ConfigParser()
    default_config.read('indexing.cfg')
    local_config_paths = default_config.items('local_config_path')

    user_config = configparser.ConfigParser()

    # We can change these hard-coded paths out for constants in the settings file
    if platform == "win32":
        env = os.getenv('APPDATA')
        env += local_config_paths[0][1]
    elif platform == "linux" or platform == "linux2":
        env = os.getenv('HOME')
        env += local_config_paths[1][1]

    try:
        user_config_file = open(env + local_config_paths[2][1])
        user_config.read_file(user_config_file)
        pass
    except FileNotFoundError:
        print("Error: User config file not found at path " + env + local_config_paths[2][1])
        sys.exit(1)
        pass
    finally:
        user_config_file.close()
    # user_config.read_file(env + 'wikitongues-language-indexing.cfg')
    default_sites = default_config.items('sites')
    user_sites = user_config.items('sites')
    if user_sites.length <= 0: # != "replace_me":
        # override sites configuration
        print("Using user configuration")
        return user_sites
    else:
        # nothing overridden. return the default config settings
        print("Using default configuration")
        return default_sites
