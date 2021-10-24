import json
from copy import deepcopy
from scraper_utils.common import write_output, recursively_count_strings, recursively_replace_keys_in_dict


def minimise_inflections(lemma_object, output_path):
    full_inflections = deepcopy(lemma_object["inflections"])

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
            full_inflections[js_key] = full_inflections[py_key]["singular"]["m"] if py_key != "imperative" else \
                full_inflections[py_key]["2nd"]["singular"]["m"]
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

    combined_keys = {
        "allSingularGenders": ["m", "f", "n"],
        "allSingularGendersExcludingNeuter": ["m", "f"],
        "allPluralGenders": ["virile", "nonvirile"]
    }

    def recursively_minimise(dic):
        for combined_key, keys in combined_keys.items():
            if keys[0] in dic and all(key in dic for key in keys):
                # This dic contains all keys of this arr, eg [m, f, n], so it let's replace with "allSingularGenders"
                # provided of course, they all contain same value.
                values = [json.dumps(dic[key]) for key in keys]
                if all(v == values[0] for v in values[1:]):
                    # They all contain the same value, eg at keys "m", "f", and "n".
                    dic[combined_key] = deepcopy(dic[keys[0]])
                    for key in keys:
                        dic.pop(key)
                    return
        for k, v in dic.items():
            if type(v) is dict:
                recursively_minimise(v)

    recursively_minimise(full_inflections)

    # STEP FOUR
    #       Modify key names "1st" to "1per", and move what needs under verbal.

    recursively_replace_keys_in_dict(full_inflections, {
        "1st": "1per",
        "2nd": "2per",
        "3rd": "3per"
    })

    res = {"inflections": full_inflections}
    res["inflections"]["verbal"] = {}
    move_to_verbal_ref = {
        "conditional": "conditional",
        "future": "future",
        "imperative": "imperative",
        "past tense": "past",
        "present tense": "present",
    }
    for py_key, js_key in move_to_verbal_ref.items():
        if py_key in res["inflections"]:
            res["inflections"]["verbal"][js_key] = res["inflections"][py_key]
            res["inflections"].pop(py_key)

    # STEP FIVE
    #       Return

    write_output(dict=res, output_file=output_path)


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
