import copy
from scraper_utils.common import recursively_count_strings, recursively_replace_keys_in_dict, recursively_minimise


def minimise_inflections(lemma_object):
    full_inflections = copy.deepcopy(lemma_object["inflections"])

    # STEP ZERO
    #       Modify key names "1st" to "1per".

    recursively_replace_keys_in_dict(full_inflections, {
        "masculine": "m",
        "feminine": "f",
        "neuter": "n",
        "1st": "1per",
        "2nd": "2per",
        "3rd": "3per",
        "future tense": "future",
    })

    full_inflections["infinitive"] = full_inflections["infinitive"]["singular"]["m"]
    if "verbal noun" in full_inflections:
        full_inflections["verbalNoun"] = full_inflections["verbal noun"]["singular"]["m"]
        full_inflections.pop("verbal noun")

    # STEP ONE
    #       Adverbials and Adjectivals

    adverbials_ref = {
        "active adjectival participle": "activeAdjectival",
        "passive adjectival participle": "passiveAdjectival",
        "contemporary adverbial participle": "contemporaryAdverbial",
        "anterior adverbial participle": "anteriorAdverbial",
        "imperative": "imperative",
    }

    for py_key, js_key in adverbials_ref.items():
        if py_key in full_inflections and full_inflections[py_key]:
            full_inflections[js_key] = full_inflections[py_key]["singular"]["m"] if py_key != "imperative" \
                else full_inflections[py_key]["2per"]["singular"]["m"]
            if py_key != js_key:
                full_inflections.pop(py_key)
        else:
            full_inflections[js_key] = False

    # STEP TWO
    #       Shortcutting future and conditional for imperfective lemma objects.

    if lemma_object["lemma"] != "być":
        if lemma_object["aspect"] == "imperfective":
            tense_ref = {
                "future": ["future", 31],
                "conditional": ["conditional", 18]
            }
        elif lemma_object["aspect"] == "perfective":
            tense_ref = {
                "conditional": ["conditional", 18]
            }
        else:
            raise Exception(f'Unexpected lemma object aspect: "{lemma_object["aspect"]}".')

        for py_key, js_key_and_count in tense_ref.items():
            js_key = js_key_and_count[0]
            if js_key == "future":
                print("")
            expected_count = js_key_and_count[1]
            actual_count = recursively_count_strings(full_inflections[py_key])
            if actual_count != expected_count:
                if actual_count + 5 == expected_count:
                    with open("TODO.txt", "a") as f:
                        f.write(
                            "\n" +
                            f'"{js_key.capitalize()}" tense on "{lemma_object["lemma"]}" should have {expected_count} strings but has {actual_count}. I think the Wiktionary page was missing the "{js_key} impersonal", but nevertheless the word does have it, so I have gone ahead and minimised the "{js_key} impersonal" to True boolean. If you disagree, you must change that.'
                            + "\n"
                        )
                        f.close()
                else:
                    raise Exception(
                        f'{js_key} tense on "{lemma_object["lemma"]}" should have {expected_count} strings but has {actual_count}.')
            full_inflections[js_key] = True
            if py_key != js_key:
                full_inflections.pop(py_key)


    # STEP THREE
    #       Minimise, eg where "m", "f", "n" keys all hold same value, minimise to just "allSingularGenders" key.

    recursively_minimise(full_inflections, {
        "allSingularGenders": ["m", "f", "n"],
        "allSingularGendersExcludingNeuter": ["m", "f"],
        "allPluralGenders": ["virile", "nonvirile"]
    })

    # STEP FOUR
    #       Move some keys under verbal.

    lemma_object["inflections"] = full_inflections
    lemma_object["inflections"]["verbal"] = {}
    move_to_verbal_ref = {
        "conditional": "conditional",
        "future": "future",
        "imperative": "imperative",
        "past tense": "past",
        "present tense": "present",
    }
    for py_key, js_key in move_to_verbal_ref.items():
        if py_key in lemma_object["inflections"]:
            lemma_object["inflections"]["verbal"][js_key] = lemma_object["inflections"][py_key]
            lemma_object["inflections"].pop(py_key)
        else:
            lemma_object["inflections"]["verbal"][js_key] = False

    return lemma_object


aspect_ref = {
    "impf": "imperfective",
    "im": "imperfective",
    "imperfective": "imperfective",
    "pf": "perfective",
    "perfective": "perfective",
}

gender_translation_ref = {
    "pl": "nonvirile",
    "plural": "nonvirile",
    "nvir": "nonvirile",
    "nonvirile": "nonvirile",
    "non virile": "nonvirile",
    "m": "m3",
    "m inan": "m3",
    "m anim": "m2",
    "m pers": "m1",
    "f": "f",
    "n": "n"
}

gender_to_tags_ref = {
    "m1": ["person"],
    "m2": ["animal"],
    "m3": ["inanimate"],
    "n": ["inanimate"],
}

case_ref = {
    "nominative": "nom",
    "genitive": "gen",
    "dative": "dat",
    "accusative": "acc",
    "instrumental": "ins",
    "locative": "loc",
    "vocative": "voc",
}

test_helper_shorthand_tag_ref_noun = {
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
