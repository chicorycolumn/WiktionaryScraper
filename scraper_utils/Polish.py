import json
import copy
from scraper_utils.common import write_output, recursively_count_strings, recursively_replace_keys_in_dict, recursively_minimise


def minimise_inflections(lemma_object, output_path):
    full_inflections = copy.deepcopy(lemma_object["inflections"])

    # STEP ZERO
    #       Modify key names "1st" to "1per".

    recursively_replace_keys_in_dict(full_inflections, {
        "masculine": "m",
        "feminine": "f",
        "neuter": "n",
        "1st": "1per",
        "2nd": "2per",
        "3rd": "3per"
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

    if lemma_object["aspect"] == "imperfective" and lemma_object["lemma"] != "być":
        tense_ref = {
            "future tense": ["future", 31],
            "conditional": ["conditional", 18]
        }

        for py_key, js_key_and_count in tense_ref.items():
            js_key = js_key_and_count[0]
            expected_count = js_key_and_count[1]
            actual_count = recursively_count_strings(full_inflections[py_key])
            if actual_count != expected_count:
                raise Exception(
                    f'Future tense on "{lemma_object["lemma"]}" should have {expected_count} strings but has {actual_count}.')
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
    #       Move what needs under verbal.

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

    # STEP FIVE
    #       Return

    write_output(dict=lemma_object, output_file=output_path)


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
