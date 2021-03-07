from wikitongues.wikitongues.data_store.airtable.airtable_language_extractor import AirtableLanguageExtractor

import pytest
import json

@pytest.fixture
def extractor():
    return AirtableLanguageExtractor()

def test_extract_languages(extractor):
    with open('resources/languages.json') as f:
        json_obj = json.load(f)

    result = extractor.extract_languages_from_json(json_obj)

    assert len(result) == 3

    assert result[0].id == 'aaa'
    assert result[0].standard_name == 'Ghotuo'
    assert result[0].wikipedia_url == 'https://en.wikipedia.org/wiki/Ghotuo_language'

    assert result[1].id == 'aab'
    assert result[1].standard_name == 'Alumu-Tesu'
    assert result[1].wikipedia_url == 'https://en.wikipedia.org/wiki/Alumu_language'

    assert result[2].id == 'aac'
    assert result[2].standard_name == 'Ari'
    assert result[2].wikipedia_url == 'https://en.wikipedia.org/wiki/Ari_language_(New_Guinea)'
