from parsers.common import reorder_lemma_objects_in_result
from utils.scraping.Polish import minimise_inflections
from utils.general.common import write_output
from utils.postprocessing.Polish import generate_adjective
from utils.postprocessing.common import make_ids, add_tags_and_topics_from_shorthand, recursively_expand_tags
from testdata.test_helpers.Polish import test_helper_shorthand_tag_ref_noun

import json
import pytest


@pytest.mark.parametrize("input,expected", [
    ([
         {"lemma": "sunflux"},
         {"lemma": "blog"},
         {"lemma": "bloggo"},
         {"lemma": "sunflo"},
         {"lemma": "bloggy"},
     ],
     [
         {"lemma": "blog"},
         {"lemma": "bloggo"},
         {"lemma": "bloggy"},
         {"lemma": "sunflux"},
         {"lemma": "sunflo"},
     ])
])
def test_reorder_lemma_objects_in_result(input, expected):
    extra_lemmas_objs = [
        {"lemma": "blog", "extra_lemmas": ["bloggo", "bloggy", "blogger"], "lemma_objects": []},
        {"lemma": "sunflo", "extra_lemmas": ["sunflu", "sunflux", "sunflox"], "lemma_objects": []},
        {"lemma": "bloggy", "extra_lemmas": ["bloggo"], "lemma_objects": []},
    ]

    ordered_result = reorder_lemma_objects_in_result(input, extra_lemmas_objs)
    assert ordered_result == expected


@pytest.mark.parametrize("input_path,expected_path,wordtype", [
    ("test_nouns_to_id_1", "with_ids/nouns_with_ids_1", "nouns"),  # contains both of homonym 'zamek'
    ("test_verbs_to_id_1", "with_ids/verbs_with_ids_1", "verbs"),  # the freq, im, pf forms of pisać
    ("test_verbs_to_id_2", "with_ids/verbs_with_ids_2", "verbs")  # 'stać' which has both an im and a pf form
    # ("test_adjectives_to_id_1", "with_ids/adjectives_with_ids_1", "adjectives") #As yet unset
])
def test_make_ids(input_path, expected_path, wordtype):
    with open(f'testdata/input/{input_path}.json', "r") as f:
        input = json.load(f)
        f.close()

    with open(f'expected/{expected_path}.json', "r") as f:
        expected = json.load(f)
        f.close()

    existing_lobjs_path = f"testdata/existing/{wordtype}"

    actual = make_ids(langcode="pol", wordtype=wordtype, lemma_objects=input, existing_lobjs_path=existing_lobjs_path)

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


@pytest.mark.parametrize("input_args_sets,expected_path", [
    (
            [
                ("narodowy", ["national"], 0, ["narodowi"])
            ],
            "expected/adjectives/polish_adjectives_0"
    ),
    (
            [
                ("stary", ["old"], 1, ["starzy"], ["staro"], ["starszy"])
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
                ("czerwony", ["red"], 3, ["czerwoni"], ["czerwono"], ["czerwieńszy"])
            ],
            "expected/adjectives/polish_adjectives_3"
    ),
    (
            [
                ("narodowy", ["national"], 0, ["narodowi"]),
                ("stary", ["old"], 1, ["starzy"], ["staro"], ["starszy"]),
                ("niebieski", ["blue"], 2, ["niebiescy"], ["niebiesko"]),
                ("czerwony", ["red"], 3, ["czerwoni"], ["czerwono"], ["czerwieńszy"])
            ],
            "expected/adjectives/polish_adjectives_4"
    ),
    (
            [
                ("oogly", ["almost boogly", "a little woogly"], 0, ["oogli", "ooglji"])  # Two pluvirnoms
            ],
            "expected/adjectives/polish_adjectives_5a"
    ),
    (
            [
                ("oogly", ["almost boogly", "a little woogly"], 1, ["oogli", "ooglji"], ["ooglo", "ooglie"], ["ooglszy"])
                # Two pluvirnoms and two adverbs
            ],
            "expected/adjectives/polish_adjectives_5b"
    ),
    (
            [
                ("oogly", ["almost boogly", "a little woogly"], 2, ["oogli", "ooglji"], ["ooglo", "ooglie"])
                # Two pluvirnoms and two adverbs
            ],
            "expected/adjectives/polish_adjectives_5c"
    ),
    (
            [
                ("oogly", ["almost boogly", "a little woogly"], 3, ["oogli", "ooglji"], ["ooglo", "ooglie"], ["ooglszy", "booglszy"])
                # Two pluvirnoms and two adverbs
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
            {"lemma": "chair", "tags": "hk"},  # Nested tags.
            {
                "lemma": "chair",
                "tags": ["concrete", "holdable", "household object"],
                "topics": ["home", "inside", "kitchen"]
            }
    ),
    (
            {"lemma": "vodka", "tags": "da"},  # Nested tags.
            {
                "lemma": "vodka",
                "tags": ["alcoholic", "concrete", "drink", "holdable"],
                "topics": ["inside", "kitchen", "nightclub", "restaurant"],
            }
    ),
    (
            {"lemma": "sand", "tags": "u,h,n"},  # Unrelated tags.
            {
                "lemma": "sand",
                "tags": ["concrete", "holdable", "natural", "uncountable"],
                "topics": ["outside"],
            }
    ),
    (
            {"lemma": "oogly", "tags": "S,A,C,Q"},
            {
                "lemma": "oogly",
                "tags": ['abstract', 'animal', 'bar', 'chemical', 'concrete', 'living', 'material', 'pet',
                         'schoolsubject', 'uncountable'],
                "topics": ['home', 'inside', 'school', 'science'],
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
