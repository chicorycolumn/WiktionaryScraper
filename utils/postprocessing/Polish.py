from copy import deepcopy
from utils.postprocessing.common import recursively_prefix_string_values, recursively_combine_string_values_into_tobjs


def get_regular_comparative_and_superlative(comparative):
    com_mod_1 = comparative[0:-1]
    pluvirnom_com = comparative[0:-2] + "i"
    comparative_regular = {
        "singular": {
            "m1": {
                "nom": f"{comparative}",
                "gen": f"{com_mod_1}ego",
                "dat": f"{com_mod_1}emu",
                "acc": f"{com_mod_1}ego",
                "ins": f"{comparative}m",
                "loc": f"{comparative}m",
            },
            "m3": {
                "nom": f"{comparative}",
                "gen": f"{com_mod_1}ego",
                "dat": f"{com_mod_1}emu",
                "acc": f"{comparative}",
                "ins": f"{comparative}m",
                "loc": f"{comparative}m",
            },
            "f": {
                "nom": f"{com_mod_1}a",
                "gen": f"{com_mod_1}ej",
                "dat": f"{com_mod_1}ej",
                "acc": f"{com_mod_1}ą",
                "ins": f"{com_mod_1}ą",
                "loc": f"{com_mod_1}ej",
            },
            "n": {
                "nom": f"{com_mod_1}e",
                "gen": f"{com_mod_1}ego",
                "dat": f"{com_mod_1}emu",
                "acc": f"{com_mod_1}e",
                "ins": f"{comparative}m",
                "loc": f"{comparative}m",
            },
        },
        "plural": {
            "virile": {
                "nom": f"{pluvirnom_com}",
                "gen": f"{comparative}ch",
                "dat": f"{comparative}m",
                "acc": f"{comparative}ch",
                "ins": f"{comparative}mi",
                "loc": f"{comparative}ch",
            },
            "nonvirile": {
                "nom": f"{com_mod_1}e",
                "gen": f"{comparative}ch",
                "dat": f"{comparative}m",
                "acc": f"{com_mod_1}e",
                "ins": f"{comparative}mi",
                "loc": f"{comparative}ch",
            },
        },
    }
    superlative_regular = deepcopy(comparative_regular)
    recursively_prefix_string_values(superlative_regular, "naj")
    return [comparative_regular, superlative_regular]


def combine_inflection_into_tobjs(arr):
    for el in arr:
        print("swde2",el)
    both = arr[0]
    print("both",both)
    for subsequent in arr[1:]:
        recursively_combine_string_values_into_tobjs(both, subsequent)
    return both


def generate_adjective(lemma: str, translations_list: list, comparative_type: int, pluvirnom_lemma: list, adverb: list = [], comparative_list: list = [], lemma_object: dict = None):
    # comparative_type     comparative_list   ...
    #          0           ['narodowy']       is NOT COMPARABLE (but may or may not have adverb).
    #          1           ['stary']          has REGULAR comparative+superlative (starszy, najstarszy) - can handle multiple eg comparative_list = ['mądrzejszy', 'mędrszy']
    #          2           ['niebieski']      has COMPOUND comparative+superlative (bardziej niebieski, najbardziej niebieski).
    #          3           ['czerwony']       has REGULAR AND COMPOUND comparative+superlative.

    lemma_mod_1 = lemma[0:-1] if lemma[-1] == "y" else lemma
    lemma_mod_2 = lemma[0:-1]

    if not lemma_object:
        lemma_object = {
            "translations": {"ENG": translations_list},
            "tags": "xxxxxxxxx",
            "lemma": lemma,
            "id": None,
        }
    lemma_object["inflections"] = {}

    simple = {
        "singular": {
            "m1": {
                "nom": f"{lemma}",
                "gen": f"{lemma_mod_1}ego",
                "dat": f"{lemma_mod_1}emu",
                "acc": f"{lemma_mod_1}ego",
                "ins": f"{lemma}m",
                "loc": f"{lemma}m",
            },
            "m3": {
                "nom": f"{lemma}",
                "gen": f"{lemma_mod_1}ego",
                "dat": f"{lemma_mod_1}emu",
                "acc": f"{lemma}",
                "ins": f"{lemma}m",
                "loc": f"{lemma}m",
            },
            "f": {
                "nom": f"{lemma_mod_2}a",
                "gen": f"{lemma_mod_1}ej",
                "dat": f"{lemma_mod_1}ej",
                "acc": f"{lemma_mod_2}ą",
                "ins": f"{lemma_mod_2}ą",
                "loc": f"{lemma_mod_1}ej",
            },
            "n": {
                "nom": f"{lemma_mod_1}e",
                "gen": f"{lemma_mod_1}ego",
                "dat": f"{lemma_mod_1}emu",
                "acc": f"{lemma_mod_1}e",
                "ins": f"{lemma}m",
                "loc": f"{lemma}m",
            },
        },
        "plural": {
            "virile": {
                "nom": pluvirnom_lemma[0] if len(pluvirnom_lemma) == 1 else {
                    "isTerminus": True,
                    "normal": pluvirnom_lemma,
                    "additionalInfrequent": []
                },
                "gen": f"{lemma}ch",
                "dat": f"{lemma}m",
                "acc": f"{lemma}ch",
                "ins": f"{lemma}mi",
                "loc": f"{lemma}ch",
            },
            "nonvirile": {
                "nom": f"{lemma_mod_1}e",
                "gen": f"{lemma}ch",
                "dat": f"{lemma}m",
                "acc": f"{lemma_mod_1}e",
                "ins": f"{lemma}mi",
                "loc": f"{lemma}ch",
            },
        },
    }

    comparative_inflections = []
    superlative_inflections = []

    if comparative_type in [1, 3]:
        for compt in comparative_list:
            cs_data = get_regular_comparative_and_superlative(compt)
            comparative_inflections.append(cs_data[0])
            superlative_inflections.append(cs_data[1])

    if comparative_type in [2, 3]:
        comparative_compound = deepcopy(simple)
        recursively_prefix_string_values(comparative_compound, "bardziej ")
        superlative_compound = deepcopy(comparative_compound)
        recursively_prefix_string_values(superlative_compound, "naj")
        comparative_inflections.append(comparative_compound)
        superlative_inflections.append(superlative_compound)

    lemma_object["inflections"]["simple"] = simple

    if adverb:
        lemma_object["inflections"]["adverb"] = adverb[0] if len(adverb) == 1 else {
                    "isTerminus": True,
                    "normal": adverb,
                    "additionalInfrequent": []
                }

    if comparative_type:
        lemma_object["inflections"]["comparative"] = combine_inflection_into_tobjs(comparative_inflections)
        lemma_object["inflections"]["superlative"] = combine_inflection_into_tobjs(superlative_inflections)

    for unneeded_key in ["comparative", "comparative_type", "pluvirnom_lemma"]:
        if unneeded_key in lemma_object:
            lemma_object.pop(unneeded_key)

    return lemma_object
