from parsers.common import scrape_word_data
from utils.scraping.Polish import minimise_inflections
from utils.general.common import write_output
from utils.postprocessing.Polish import generate_adjective
from utils.postprocessing.common import make_ids, add_tags_and_topics_from_shorthand, recursively_expand_tags
from testdata.test_helpers.Polish import test_helper_shorthand_tag_ref_noun

import json
import pytest
import os


@pytest.mark.parametrize("input_path,expected_path,wordtype", [
    # ("test_nouns_to_id_1", "with_ids/nouns_with_ids_1", "nouns"),
    ("test_verbs_to_id_1", "with_ids/verbs_with_ids_1", "verbs")
])
def test_make_ids(input_path, expected_path, wordtype):
    with open(f'testdata/input/{input_path}.json', "r") as f:
        input = json.load(f)
        f.close()

    with open(f'expected/{expected_path}.json', "r") as f:
        expected = json.load(f)
        f.close()

    existing_lemma_objects = []
    path = f"testdata/existing/{wordtype}"
    for root, dirs, files in os.walk(path):
        for file in files:
            print(file)
            with open(f'{path}/{file}', "r") as f:
                loaded = json.load(f)
                existing_lemma_objects.extend(loaded)
                f.close()

    actual = make_ids(langcode="pol", wordtype=wordtype, lemma_objects=input, existing_lemma_objects=existing_lemma_objects)

    write_output(actual, expected_path.split("/")[-1])

    with open(f'output/{expected_path.split("/")[-1]}.json', "r") as f:
        actual = json.load(f)
        f.close()

    assert actual == expected


@pytest.mark.parametrize("input_path,expected_path", [
    ("parsed_polish_protoverbs_0", "minimised_polish_verbs_0"),  # impf frequentative: pisywać
    ("parsed_polish_protoverbs_1", "minimised_polish_verbs_1"),  # impf: pisać
    ("parsed_polish_protoverbs_2", "minimised_polish_verbs_2"),  # pf: napisać
    ("parsed_polish_protoverbs_3", "minimised_polish_verbs_3"),  # impf: czytać
    ("parsed_polish_protoverbs_4", "minimised_polish_verbs_4"),  # pf: przeczytać
    ("parsed_polish_protoverbs_5", "minimised_polish_verbs_5"),  # various: badać, zbadać, widzieć, zobaczyć
])
def test_polish_verb_minimiser(input_path: str, expected_path: str, wordtype: str = "verbs"):
    with open(f'expected/{wordtype}/{expected_path}.json', 'r') as f:
        expected = json.load(f)
        f.close()

    with open(f'expected/{wordtype}/{input_path}.json', 'r') as f:
        input = json.load(f)
        f.close()

    minimised_verbs = [minimise_inflections(protoverb) for protoverb in input]

    write_output(dict=minimised_verbs, output_file=expected_path)

    with open(f'output/{expected_path}.json', 'r') as f:
        actual = json.load(f)
        f.close()

    actual = [obj["inflections"] for obj in actual]
    expected = [obj["inflections"] for obj in expected]

    assert actual == expected


@pytest.mark.parametrize("input_words,expected_path,use_sample", [
    (["pisywać"], "parsed_polish_protoverbs_0", True),  # impf frequentative
    (["pisać"], "parsed_polish_protoverbs_1", True),  # impf
    (["napisać"], "parsed_polish_protoverbs_2", True),  # pf
    (["czytać"], "parsed_polish_protoverbs_3", True),  # impf
    (["przeczytać"], "parsed_polish_protoverbs_4", True),  # pf
    (["badać", "zbadać", "widzieć", "zobaczyć"], "parsed_polish_protoverbs_5", True),  # various
])
def test_PolishVerbParser(input_words: list, expected_path: str, use_sample: bool, wordtype: str = "verbs"):
    print(f'# Starting, given {len(input_words)} words.')

    output_path = f"output_test{expected_path[-2:]}"
    rejected_path = f"rejected_test{expected_path[-2:]}"
    expected_rejected_path = f"rejected_{expected_path}"

    with open(f'expected/{wordtype}/{expected_path}.json', 'r') as f:
        expected = json.load(f)
        f.close()

    scrape_word_data(
        language="Polish",
        head_words=input_words,
        use_sample=use_sample,
        wordtype=wordtype,
        filepaths={
            "output": output_path,
            "rejected": rejected_path,
        },
        group_number=0,
        no_temp_ids=True
    )

    with open(f'output/{output_path}_scraped.json', 'r') as f:
        actual = json.load(f)
        f.close()

    assert actual == expected

    with open(f'expected/{wordtype}/{expected_rejected_path}.json', 'r') as f:
        expected_rejected = json.load(f)
        f.close()

    with open(f'output/{rejected_path}.json', 'r') as f:
        actual_rejected = json.load(f)
        f.close()

    assert actual_rejected == expected_rejected


@pytest.mark.parametrize("input_words,expected_path,use_sample", [
    (["narodowy"], "polish_protoadjectives_0", True),
    (["stary"], "polish_protoadjectives_1", True),
    (["niebieski"], "polish_protoadjectives_2", True),
    (["czerwony"], "polish_protoadjectives_3", True),
    (["czerwony", "niebieski", "stary", "narodowy"], "polish_protoadjectives_4", True),
    (["czerwony", "BADWORD", "stary", "narodowy"], "polish_protoadjectives_5", False),
    (["czerwony", "kobieta", "stary", "narodowy"], "polish_protoadjectives_6", False),
    (["zielony"], "polish_protoadjectives_7", False),
    (["średniowieczny", "śródziemnomorski"], "polish_protoadjectives_8", True)
])
def test_PolishAdjectiveParser(input_words: list, expected_path: str, use_sample: bool, wordtype: str = "adjectives"):
    print(f'# Starting, given {len(input_words)} words.')

    output_path = f"output_test{expected_path[-2:]}"
    rejected_path = f"rejected_test{expected_path[-2:]}"
    expected_rejected_path = f"rejected_{expected_path}"

    with open(f'expected/{wordtype}/{expected_path}.json', 'r') as f:
        expected = json.load(f)
        f.close()

    scrape_word_data(
        language="Polish",
        head_words=input_words,
        use_sample=use_sample,
        wordtype=wordtype,
        filepaths={
            "output": output_path,
            "rejected": rejected_path,
        },
        group_number=0,
        no_temp_ids=True
    )

    with open(f'output/{output_path}_scraped.json', 'r') as f:
        actual = json.load(f)
        f.close()

    assert actual == expected

    with open(f'expected/{wordtype}/{expected_rejected_path}.json', 'r') as f:
        expected_rejected = json.load(f)
        f.close()

    with open(f'output/{rejected_path}.json', 'r') as f:
        actual_rejected = json.load(f)
        f.close()

    assert actual_rejected == expected_rejected


@pytest.mark.parametrize("input_args_sets,expected_path", [
    (
            [
                ("narodowy", ["national"], 0, ["narodowi"])
            ],
            "expected/adjectives/polish_adjectives_0"
    ),
    (
            [
                ("stary", ["old"], 1, ["starzy"], ["staro"], "starszy")
            ],
            "expected/adjectives/polish_adjectives_1"
    ),
    (
            [
                ("niebieski", ["blue"], 2, ["niebiescy"], ["niebiesko"])
            ],
            "expected/adjectives/polish_adjectives_2"
    ),
    (
            [
                ("czerwony", ["red"], 3, ["czerwoni"], ["czerwono"], "czerwieńszy")
            ],
            "expected/adjectives/polish_adjectives_3"
    ),
    (
            [
                ("narodowy", ["national"], 0, ["narodowi"]),
                ("stary", ["old"], 1, ["starzy"], ["staro"], "starszy"),
                ("niebieski", ["blue"], 2, ["niebiescy"], ["niebiesko"]),
                ("czerwony", ["red"], 3, ["czerwoni"], ["czerwono"], "czerwieńszy")
            ],
            "expected/adjectives/polish_adjectives_4"
    ),
    (
            [
                ("oogly", ["almost boogly", "a little woogly"], 0, ["oogli", "ooglji"])
            ],
            "expected/adjectives/polish_adjectives_5a"
    ),
    (
            [
                ("oogly", ["almost boogly", "a little woogly"], 1, ["oogli", "ooglji"], ["ooglo", "ooglie"], "ooglszy")
            ],
            "expected/adjectives/polish_adjectives_5b"
    ),
    (
            [
                ("oogly", ["almost boogly", "a little woogly"], 2, ["oogli", "ooglji"], ["ooglo", "ooglie"])
            ],
            "expected/adjectives/polish_adjectives_5c"
    ),
    (
            [
                ("oogly", ["almost boogly", "a little woogly"], 3, ["oogli", "ooglji"], ["ooglo", "ooglie"], "ooglszy")
            ],
            "expected/adjectives/polish_adjectives_5d"
    ),
])
def test_generate_adjective(input_args_sets: list, expected_path: str):
    with open(f"{expected_path}.json", "r") as f:
        expected_adjectives = json.load(f)
        f.close()

    actual_adjectives = [generate_adjective(*input_args) for input_args in input_args_sets]

    write_output(actual_adjectives, expected_path.split("/")[-1], "output")

    assert actual_adjectives == expected_adjectives


@pytest.mark.parametrize("lemma_object,expected_lemma_object", [
    (
            {"lemma": "chair", "tags": "hk"},
            {
                "lemma": "chair",
                "tags": ["concrete", "holdable", "household object"],
                "topics": ["home", "inside", "kitchen"]
            }
    ),
    (
            {"lemma": "vodka", "tags": "da"},
            {
                "lemma": "vodka",
                "tags": ["alcoholic", "concrete", "drink", "holdable"],
                "topics": ["inside", "kitchen", "nightclub", "restaurant"],
            }
    ),
    (
            {"lemma": "sand", "tags": "u,h,n"},
            {
                "lemma": "sand",
                "tags": ["concrete", "holdable", "natural", "uncountable"],
                "topics": ["outside"],
            }
    ),
])
def test_add_tags_and_topics_from_shorthand(lemma_object: object, expected_lemma_object: object):
    add_tags_and_topics_from_shorthand(lemma_object, test_helper_shorthand_tag_ref_noun)
    assert lemma_object == expected_lemma_object


@pytest.mark.parametrize("input_stags,expected_output_tags", [
    (["c"], ["citrus", "fruit", "sweet", "food"]),
    (["o"], ["lends its name to a color", "citrus", "fruit", "sweet", "food"]),
    (["c", "y"], ["yellow", "citrus", "fruit", "sweet", "food"]),
    (["v", "r"], ["red", "vegetable", "savoury", "food"])
])
def test_recursively_expand_tags(input_stags: list, expected_output_tags: list):
    ref = {
        "f": {"tags": ["food"]},
        "fr": {"tags": ["f", "fruit", "sweet"]},
        "v": {"tags": ["f", "vegetable", "savoury"]},
        "c": {"tags": ["fr", "citrus"]},
        "o": {"tags": ["c", "lends its name to a color"]},
        "y": {"tags": ["yellow"]},
        "r": {"tags": ["red"]}
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
def test_PolishNounParser(input_words: list, expected_path: str, use_sample: bool, wordtype: str = "nouns"):
    print(f'# Starting, given {len(input_words)} words.')

    output_path = f"output_test{expected_path[-2:]}"
    rejected_path = f"rejected_test{expected_path[-2:]}"
    expected_rejected_path = f"rejected_{expected_path}"

    with open(f'expected/{wordtype}/{expected_path}.json', 'r') as f:
        expected = json.load(f)
        f.close()

    scrape_word_data(
        language="Polish",
        head_words=input_words,
        use_sample=use_sample,
        wordtype=wordtype,
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

    with open(f'expected/{wordtype}/{expected_rejected_path}.json', 'r') as f:
        expected_rejected = json.load(f)
        f.close()

    with open(f'output/{rejected_path}.json', 'r') as f:
        actual_rejected = json.load(f)
        f.close()

    assert actual_rejected == expected_rejected
