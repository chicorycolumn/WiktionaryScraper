import pytest
from parser_classes.Polish_parsers import PolishNounHTMLParser
from scraper_utils.common import scrape_word_data
from input.Polish.input_words import nouns_1


@pytest.mark.parametrize("input_words,expected_path,use_sample,skip_comparison", [
    (["baba", "bałagan", "cel", "drzwi", "dzień", "małpa", "miesiąc", "rok", "ser"], "polish_nouns_1", True, False),
    (["prysznic", "glista", "gleba", "łeb", "BADWORD", "palec", "noga", "piła", "piłka"], "polish_nouns_2", False, False),
    (["nadzieja", "słońce", "wieczór", "sierpień", "ból", "złodziej", "wartość", "owca", "suszarka", "schody"], "polish_nouns_3", True, False),
    (["prysznic", "BADWORD", "ANOTHERBADWORD", "glista"], "polish_nouns_4", False, False),
    # (nouns_1[0:2], "polish_nouns_5", False, True)
])
def test_PolishNounHTMLParser(input_words: list, expected_path: str, use_sample: bool, skip_comparison: bool):
    output_path = f"output_test{expected_path[-2:]}"
    rejected_path = f"rejected_test{expected_path[-2:]}"

    if not skip_comparison:
        with open(f'expected/{expected_path}.json', 'r') as f:
            expected = f.read()
            f.close()

    scrape_word_data(
        "Polish",
        PolishNounHTMLParser(convert_charrefs=False),
        input_words,
        use_sample,
        output_path,
        rejected_path
    )

    with open(f'output/{output_path}.json', 'r') as f:
        actual = f.read()
        f.close()

    if skip_comparison:
        print("\n# Finished scraping for these words:", input_words)
    else:
        assert actual == expected
