from parsers.common import scrape_word_data
from utils.scraping.Polish import minimise_inflections
from utils.general.common import write_output
from utils.postprocessing.Polish import generate_adjective
from utils.postprocessing.common import make_ids, add_tags_and_topics_from_shorthand, recursively_expand_tags
from testdata.test_helpers.Polish import test_helper_shorthand_tag_ref_noun

import json
import pytest
import os


@pytest.mark.parametrize("input_words,expected_path,use_sample,skip_extras", [
    (["pisywać"], "parsed_polish_protoverbs_0", True, True),            # impf frequentative
    (["pisać"], "parsed_polish_protoverbs_1", True, True),              # impf
    (["napisać"], "parsed_polish_protoverbs_2", True, True),            # pf
    (["czytać"], "parsed_polish_protoverbs_3", True, True),             # impf
    (["przeczytać"], "parsed_polish_protoverbs_4", True, True),         # pf
    (["badać", "zobaczyć", "zbadać", "widzieć", "widywać"], "parsed_polish_protoverbs_5", True, True), # various
    (["badać", "zobaczyć"], "parsed_polish_protoverbs_5", True, False), # Testing the additional parsing of otherShapes.
    (["stać"], "parsed_polish_protoverbs_6", True, True),               # Verb has two meanings and two conj tables
    (["kopać"], "parsed_polish_protoverbs_7", True, True),              # Allohom! Verb has two meanings and one conj table
    (["brać"], "parsed_polish_protoverbs_8", True, True),               # Page contains one noun one verb, homonyms (not nec to list as allohoms as are diff wordtypes).
    (["chodzić"], "parsed_polish_protoverbs_9", True, True),            # Verb has two meanings and two conj tables like stać but was tripping up.
])
def test_PolishVerbParser(input_words: list, expected_path: str, use_sample: bool, skip_extras: bool, wordtype: str = "verbs"):
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
        no_temp_ids=True,
        skip_extras=skip_extras
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
    (["narodowy"], "polish_protoadjectives_0", True),  # type 1
    (["stary"], "polish_protoadjectives_1", True),  # type 2
    (["niebieski"], "polish_protoadjectives_2", True),  # type 3
    (["czerwony"], "polish_protoadjectives_3", True),  # type 4
    (["czerwony", "niebieski", "stary", "narodowy"], "polish_protoadjectives_4", True),  # types 1-4
    (["czerwony", "BADWORD", "stary", "narodowy"], "polish_protoadjectives_5", False),  # contains failing word
    (["czerwony", "kobieta", "stary", "narodowy"], "polish_protoadjectives_6", False),  # contains noun
    (["zielony"], "polish_protoadjectives_7", False),  # type 2
    (["średniowieczny", "śródziemnomorski"], "polish_protoadjectives_8", True)  # less common adjective
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


@pytest.mark.parametrize("n,input_words,expected_path,use_sample", [
    (1, ["baba", "bałagan", "cel", "drzwi", "dzień", "małpa", "miesiąc", "rok", "ser"], "polish_nouns_1", True), # Normal words
    (2, ["nadzieja", "słońce", "wieczór", "sierpień", "ból", "złodziej", "wartość", "owca", "suszarka", "schody"], "polish_nouns_2", True),  # Normal words
    (3, ["prysznic", "glista", "gleba", "łeb", "BADWORD", "palec", "noga", "piła", "piłka"], "polish_nouns_3", False), # Some failing words
    (4, ["prysznic", "BADWORD", "ANOTHERBADWORD", "glista"], "polish_nouns_4", False),  # Some failing words
    (5, ["prysznic", "polski", "glista"], "polish_nouns_5", False),  # Some failing words
    (6, ["kapusta"], "polish_nouns_6", True),  # Word with two meanings and two conjugation tables
    (7, ["brać"], "polish_nouns_7", True),  # Word's page has one verb one noun, homonyms (not nec to list as allohoms as are diff wordtypes).
])
def test_PolishNounParser(n: int, input_words: list, expected_path: str, use_sample: bool, wordtype: str = "nouns"):
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
