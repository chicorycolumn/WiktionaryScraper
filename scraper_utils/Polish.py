import json
from copy import deepcopy
from scraper_utils.common import write_output


def minimise_inflections(lemma_object, output_path):
    full_inflections = deepcopy(lemma_object["inflections"])
    res = {"verbal": {"past": {}, "present": {}, "future": {}, "conditional": {}, "imperative": {}}}
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

    res["inflections"] = full_inflections

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
