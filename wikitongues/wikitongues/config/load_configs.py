import sys
from sys import platform
import configparser
import os


def load_configs():

    print("loading config file")

    default_config = configparser.ConfigParser()
    current_dir = os.path.dirname(__file__)
    default_config.read_file(open(os.path.join(current_dir,"indexing.cfg")))
    local_config_paths = default_config.items("local_config_path")

    user_config = configparser.ConfigParser()

    if platform == "windows":
        env = os.getenv("APPDATA")
        env += local_config_paths[0][1]
    elif platform == "linux" or platform == "linux2" or platform == "darwin":
        env = os.getenv("HOME")
        env += local_config_paths[1][1]
    else:
        raise Exception("This program is intended only for Mac,"
                        + "Linux, or Windows machines.")

    try:
        user_config_file = open(env + local_config_paths[2][1])
        user_config.read_file(user_config_file)
        user_config_file.close()
        pass
    except FileNotFoundError:
        print("Error: User config file not found at path "
              + env
              + local_config_paths[2][1])
        sys.exit(1)
        pass

    if len(user_config.items("sites")) > 0:
        # override sites configuration
        print("Using user configuration")
        return user_config
    else:
        # nothing overridden. return the default config settings
        print("Using default configuration")
        return default_config
