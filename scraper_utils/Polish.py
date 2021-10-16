
def make_inflection_skeleton(lemma_object):
    full_inflections = lemma_object["inflections"]

    res = {"verbal": {}}

    def get_value_same_for_all_keys(key, final_key = None):

        if not final_key:
            final_key = key

        arr = [
            full_inflections[key]["singular"]["masculine"],
            full_inflections[key]["singular"]["feminine"],
            full_inflections[key]["singular"]["neuter"],
            full_inflections[key]["plural"]["virile"],
            full_inflections[key]["plural"]["nonvirile"],
        ]

        if not all(w == arr[0] for w in arr):
            raise Exception("#ERR Infinitives not all the same.")

        res[final_key] = arr[0]

    get_value_same_for_all_keys("infinitive")
    get_value_same_for_all_keys("passiveAdjectival", "passiveAdjectival")
    get_value_same_for_all_keys("verbalNoun", "verbalNoun")

    if lemma_object["aspect"] == "imperfective":
        get_value_same_for_all_keys("activeAdjectival", "activeAdjectival")
        get_value_same_for_all_keys("anteriorAdverbial", "anteriorAdverbial")
        get_value_same_for_all_keys("contemporaryAdverbial", "contemporaryAdverbial")
    elif lemma_object["aspect"] == "perfective":
        get_value_same_for_all_keys("activeAdjectival", "activeAdjectival")
        get_value_same_for_all_keys("anteriorAdverbial", "anteriorAdverbial")
        get_value_same_for_all_keys("contemporaryAdverbial", "contemporaryAdverbial")
    else:
        raise ValueError("#ERR Is neither perfective nor imperfective.")


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
