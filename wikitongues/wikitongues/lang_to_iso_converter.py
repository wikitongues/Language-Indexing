from abc import ABC, abstractmethod

import languagecodes


class ILangToIsoConverter(ABC):
    """
    Interface for converting html lang attribute to ISO 639-3 code

    Args:
        ABC
    """

    @abstractmethod
    def get_iso_code(self, lang_attribute: str) -> str:
        """
        Converts html lang attribute to ISO 639-3 code

        Args:
            lang_attribute (str): lang attribute
        """
        pass


class LangToIsoConverter(ILangToIsoConverter):
    """
    Converts html lang attribute to ISO 639-3 code

    Args:
        ILangToIsoConverter
    """

    def get_iso_code(self, lang_attribute: str) -> str:
        """[summary]
        Converts html lang attribute to ISO 639-3 code

        Args:
            lang_attribute (str): lang attribute

        Returns:
            str: ISO 639-3 code
        """
        # https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/lang
        language_subtag = lang_attribute.split("-")[0]
        return languagecodes.iso_639_alpha3(language_subtag)
