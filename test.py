import pytest
from parsers.Polish_adjective_parser import *
from parsers.Polish_noun_parser import *
from parsers.Polish_verb_parser import *
from scraper_utils.processing import *
from scraper_utils.Polish import minimise_inflections
from semimanual_utils.Polish import *

@pytest.mark.parametrize("input_path,expected_path", [
    # (["pisywać"], "polish_protoverbs_0", True), #impf freq
    # (["pisać"], "polish_protoverbs_1", True), #impf
    # (["napisać"], "polish_protoverbs_2", True), #pf
    ("parsed_protoverb_3", "minimised_polish_verb_3"), #impf
    # (["przeczytać"], "polish_protoverbs_4", True), #pf
    # (["badać", "zbadać", "widzieć", "zobaczyć"], "polish_protoverbs_5", True),
])
def test_verb_minimiser(input_path: str, expected_path: str, wordtype: str = "verbs"):
    with open(f'expected/{wordtype}/{expected_path}.json', 'r') as f:
        expected = json.load(f)
        f.close()

    with open(f'input/Polish/{wordtype}/{input_path}.json', 'r') as f:
        input = json.load(f)
        f.close()

    minimise_inflections(input, expected_path)

    with open(f'output/{expected_path}.json', 'r') as f:
        actual = json.load(f)
        f.close()

    assert actual["inflections"] == expected["inflections"]


@pytest.mark.parametrize("input_words,expected_path,use_sample", [
    # (["pisywać"], "polish_protoverbs_0", True), #impf freq
    # (["pisać"], "polish_protoverbs_1", True), #impf
    # (["napisać"], "polish_protoverbs_2", True), #pf
    (["czytać"], "polish_protoverbs_3", True), #impf
    # (["przeczytać"], "polish_protoverbs_4", True), #pf
    # (["badać", "zbadać", "widzieć", "zobaczyć"], "polish_protoverbs_5", True),
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
        parser=PolishVerbParser(convert_charrefs=False),
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
        parser=PolishAdjectiveParser(convert_charrefs=False),
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
])
def test_generate_adjective(input_args_sets: list, expected_path: str):
    with open(f"{expected_path}.json", "r") as f:
        expected_adjectives = json.load(f)
        f.close()

    actual_adjectives = [generate_adjective(*input_args) for input_args in input_args_sets]

    write_output(actual_adjectives, "polish_adjectives_4_updated", "expected/adjectives")

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
    test_shorthand_tag_ref_noun = {
        "u": {
            "tags": ["uncountable"],
            "topics": [],
        },
        "h": {
            "tags": ["holdable", "concrete"],
            "topics": [],
        },
        "m": {
            "tags": ["manmade", "concrete"],
            "topics": [],
        },
        "n": {
            "tags": ["natural", "concrete"],
            "topics": ["outside"],
        },
        "s": {
            "tags": ["school"],
            "topics": [],
        },
        "w": {
            "tags": ["work"],
            "topics": [],
        },

        # # # # # # # # # # #

        "c": {
            "tags": ["material", "uncountable", "concrete"],
            "topics": ["basic"],
        },
        "¢": {
            "tags": ["chemical", "c"],
            "topics": ["science"],
        },
        "b": {
            "tags": ["bodypart", "concrete"],
            "topics": ["at the doctor", "basic", "body"],
        },
        "ß": {
            "tags": ["schoolsubject", "abstract"],
            "topics": ["school"],
        },
        "w": {
            "tags": ["weather", "abstract", "uncountable"],
            "topics": ["basic", "outdoor"],
        },
        "!": {
            "tags": ["noise", "abstract"],
            "topics": ["sense and perception"],
        },
        "e": {
            "tags": ["emotion", "abstract"],
            "topics": ["inside your head"],
        },
        "$": {
            "tags": ["money"],
            "topics": ["shopping", "maths", "travel"],
        },
        "@": {
            "tags": ["measurement"],
            "topics": ["maths"],
        },
        "at": {
            "tags": ["abstract", "time"],
            "topics": ["travel", "maths"],
        },
        "as": {
            "tags": ["abstract"],
            "topics": ["school"],
        },
        "aw": {
            "tags": ["abstract"],
            "topics": ["work"],
        },
        "ag": {
            "tags": ["abstract"],
            "topics": ["geometric", "maths"],
        },
        "aa": {
            "tags": ["abstract"],
            "topics": [],
        },
        "r": {
            "tags": ["relative", "person", "living", "concrete"],
            "topics": ["relationships"],
        },
        "j": {
            "tags": ["profession", "person", "living", "concrete"],
            "topics": ["work"],
        },
        "a": {
            "tags": ["animal", "living", "concrete"],
            "topics": ["outside"],
        },
        "æ": {
            "tags": ["pet", "animal", "living", "concrete"],
            "topics": ["home", "inside"],
        },
        "t": {
            "tags": ["title", "person", "living", "concrete"],
            "topics": [],
        },
        "p": {
            "tags": ["person", "living", "concrete"],
            "topics": [],
        },
        "f": {
            "tags": ["food", "h"],
            "topics": ["kitchen", "restaurant", "inside"],
        },
        "d": {
            "tags": ["drink", "h"],
            "topics": ["kitchen", "restaurant", "inside"],
        },
        "da": {
            "tags": ["alcoholic", "d"],
            "topics": ["kitchen", "restaurant", "nightclub", "inside"],
        },
        "g": {
            "tags": ["clothes", "h"],
            "topics": ["basic"],
        },
        "lg": {
            "tags": ["location", "concrete"],
            "topics": [],
        },
        "lb": {
            "tags": ["location", "building", "concrete"],
            "topics": ["inside"],
        },
        "lr": {
            "tags": ["location", "room", "concrete"],
            "topics": ["inside"],
        },
        "ln": {
            "tags": ["location", "natural", "concrete"],
            "topics": ["outside"],
        },
        "ls": {
            "tags": ["special location", "abstract"],
            "topics": ["religion"],
        },
        "hf": {
            "tags": ["furniture", "concrete"],
            "topics": ["home", "inside"],
        },
        "hh": {
            "tags": ["household object", "h"],
            "topics": ["home", "inside"],
        },
        "hf": {
            "tags": ["furniture", "concrete"],
            "topics": ["home", "inside"],
        },
        "hb": {
            "tags": ["hh"],
            "topics": ["home", "inside", "bedroom"],
        },
        "hk": {
            "tags": ["hh"],
            "topics": ["home", "inside", "kitchen"],
        },
        "hw": {
            "tags": ["hh"],
            "topics": ["home", "inside", "washroom"],
        },
        "hp": {
            "tags": ["part of house", "concrete"],
            "topics": ["home", "inside"],
        }
    }

    add_tags_and_topics_from_shorthand(lemma_object, test_shorthand_tag_ref_noun)

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
    (["nadzieja", "słońce", "wieczór", "sierpień", "ból", "złodziej", "wartość", "owca", "suszarka", "schody"], "polish_nouns_2", True),
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
        parser=PolishNounParser(convert_charrefs=False),
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
