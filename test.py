import pytest
import json
from parser_classes.Polish_parsers import PolishNounHTMLParser
from scraper_utils.processing import *
from input.Polish.input_words import nouns_1


@pytest.mark.parametrize("input_stags,expected_output_tags", [
    (["c"], ["citrus", "fruit", "sweet", "food"]),
    (["o"], ["lends its name to a color", "citrus", "fruit", "sweet", "food"]),
    (["c", "y"], ["yellow", "citrus", "fruit", "sweet", "food"]),
    (["v", "r"], ["red", "vegetable", "savoury", "food"])
])
def test_recursively_expand_tags(input_stags: list, expected_output_tags: list):
    ref = {
        "f": {"tags":["food"]},
        "fr": {"tags":["f", "fruit", "sweet"]},
        "v": {"tags":["f", "vegetable", "savoury"]},
        "c": {"tags":["fr", "citrus"]},
        "o": {"tags":["c", "lends its name to a color"]},
        "y": {"tags":["yellow"]},
        "r": {"tags":["red"]}
    }

    actual_output_tags = recursively_expand_tags(input_stags, ref)

    actual_output_tags.sort()
    expected_output_tags.sort()

    assert actual_output_tags == expected_output_tags


@pytest.mark.parametrize("input_words,expected_path,use_sample", [
    (["baba", "bałagan", "cel", "drzwi", "dzień", "małpa", "miesiąc", "rok", "ser"], "polish_nouns_1", True),
    (["nadzieja", "słońce", "wieczór", "sierpień", "ból", "złodziej", "wartość", "owca", "suszarka", "schody"],
     "polish_nouns_2", True),
    (["prysznic", "glista", "gleba", "łeb", "BADWORD", "palec", "noga", "piła", "piłka"], "polish_nouns_3", False),
    (["prysznic", "BADWORD", "ANOTHERBADWORD", "glista"], "polish_nouns_4", False),
    (["prysznic", "polski", "glista"], "polish_nouns_5", False),
])
def test_PolishNounHTMLParser(input_words: list, expected_path: str, use_sample: bool):
    print(f'# Starting, given {len(input_words)} words.')

    output_path = f"output_test{expected_path[-2:]}"
    rejected_path = f"rejected_test{expected_path[-2:]}"
    expected_rejected_path = f"rejected_{expected_path}"

    with open(f'expected/{expected_path}.json', 'r') as f:
        expected = json.load(f)
        f.close()

    scrape_word_data(
        PolishNounHTMLParser(convert_charrefs=False),
        "Polish",
        input_words,
        use_sample,
        filepaths={
            "output": output_path,
            "rejected": rejected_path,
        },
        group_number=0,
        no_temp_ids=True
    )

    with open(f'output/{output_path}.json', 'r') as f:
        actual = json.load(f)
        f.close()

    assert actual == expected

    with open(f'expected/{expected_rejected_path}.json', 'r') as f:
        expected_rejected = json.load(f)
        f.close()

    with open(f'output/{rejected_path}.json', 'r') as f:
        actual_rejected = json.load(f)
        f.close()

    assert actual_rejected == expected_rejected
