# The Language class is (part of) the input to the program.
# It contains details used to locate web resources about a language.
# More fields will be added as we go.


class Language:
    # iso_code: ISO code of the language - unique to each language
    # standard_name: "Standard" name of the language
    # wikipedia_url: URL of the language's Wikipedia page
    def __init__(self, iso_code, standard_name, wikipedia_url):
        self.id = iso_code
        self.standard_name = standard_name
        self.wikipedia_url = wikipedia_url
