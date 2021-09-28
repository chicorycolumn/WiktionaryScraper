import pytest
from main import PolishNounHTMLParser
from scraper_utils.common import scrape_word_data


@pytest.mark.parametrize("input_words,expected_path,use_local_data", [
    (["baba", "bałagan", "cel", "drzwi", "dzień", "małpa", "miesiąc", "rok", "ser"], "expected_output_polish_1", True),
    (["prysznic", "glista", "gleba", "łeb", "palec", "noga", "piła", "piłka"], "expected_output_polish_2", False)
])
def test_PolishNounHTMLParser(input_words, expected_path, use_local_data):
    output_path = f"output_test{expected_path[-2:]}"

    with open(f'output/{expected_path}.json', 'r') as f:
        expected = f.read()
        f.close()

    scrape_word_data(
        "Polish",
        PolishNounHTMLParser(convert_charrefs=False),
        input_words,
        use_local_data,
        output_path
    )

    with open(f'output/{output_path}.json', 'r') as f:
        actual = f.read()
        f.close()

    assert actual == expected
