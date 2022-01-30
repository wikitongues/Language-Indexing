import os

from language_indexing_config import user_config_file


def ask_user_for_user_file_creation():
    user_file = user_config_file()
    if os.path.isfile(user_file) is True:
        overwrite = input("The user file already exist, do you want to " + "overwrite the current config file? (Y/N) ")
        if overwrite.lower() == "y":
            create_user_file(user_file)
    else:
        create_user_file(user_file)


def create_user_file(file_location):
    ask_fake = input("Do you want to connect to Airtable? (Y/N) ")
    if ask_fake.lower() == "n":
        fake = True
    else:
        fake = False

    if not fake:
        api_key = input("Enter the api key: ")
        base_id = input("Enter the base id: ")
        page_size = input("Enter the number of languages per query: ")
    else:
        api_key = ""
        base_id = ""
        page_size = "100"

    default_file = open(os.path.join(os.path.dirname(__file__), "config/indexing.cfg"), "r")
    user_file = open(file_location, "w")
    for line in default_file:
        if line.startswith("[DEFAULT]"):
            user_file.write(line)
            user_file.write("base_id : " + base_id + "\n")
            user_file.write("api_key : " + api_key + "\n")
            user_file.write("fake : " + str(fake) + "\n")
            break
        elif line.startswith("page_size"):
            user_file.write("page_size : " + page_size + "\n")
        else:
            user_file.write(line)

    print(f"Your configuration file has been written to {file_location}")
