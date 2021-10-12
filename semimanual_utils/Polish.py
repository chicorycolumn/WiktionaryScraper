from copy import deepcopy


def get_value_from_keypath(dict, keypath):
    for key in keypath:
        dict = dict[key]
    return dict


def recursively_combine_string_values_into_terminus_objects(dict1, dict2):
    # Note, dict1 values are favoured as "normal" while dict2 values will be "additionalInfrequent"

    keypath = []

    for key, value in dict1.items():
        keypath.append(key)

        if type(value) in [str, list]:
            if type(value) == str:
                normal = [value]
            elif type(value) == list:
                normal = value[:]

            dict2_value = get_value_from_keypath(dict2, keypath)

            if type(dict2_value) == str:
                additionalInfrequent = [dict2_value]
            elif type(dict2_value) == list:
                additionalInfrequent = dict2_value[:]
            else:
                raise Exception(f"Unexpected type {type(dict2_value)} at keypath {keypath}.")

            get_value_from_keypath(dict1, keypath[:-1])[key] = {
                "isTerminus": True,
                "normal": normal,
                "additionalInfrequent": additionalInfrequent
            }

        elif type(value) == dict:
            recursively_combine_string_values_into_terminus_objects(value, get_value_from_keypath(dict2, keypath))
        else:
            raise Exception(f"Unexpected type {type(dict2_value)} at keypath {keypath}.")

        keypath.pop()


def recursively_prefix_string_values(dict, prefix):
    for key, value in dict.items():
        if type(value) == str:
            dict[key] = f"{prefix}{value}"
        else:
            recursively_prefix_string_values(value, prefix)


def generate_adjective(lemma: str, translations_list: list, comparative_type: int, pluvirnom_lemma, adverb: str = None, comparative: str = None):
    # narodowy  comparative_type 0  is NOT COMPARABLE and has no adverb.
    # stary     comparative_type 1  has REGULAR comparative/superlative (starszy, najstarszy).
    # niebieski comparative_type 2  has COMPOUND comparative/superlative (bardziej niebieski, najbardziej niebieski).
    # czerwony  comparative_type 3  has REGULAR AND COMPOUND comparative/superlative.

    lemma_mod_1 = lemma[0:-1] if lemma[-1] == "y" else lemma
    lemma_mod_2 = lemma[0:-1]

    lemma_object = {
        "translations": {"ENG": translations_list},
        "tags": "xxxxxxxxx",

        "lemma": lemma,
        "id": None,

        "inflections": {}
    }
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
                "nom": f"{pluvirnom_lemma}",
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

    if comparative_type in [1, 3]:
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
    if comparative_type in [2, 3]:
        comparative_compound = deepcopy(simple)
        recursively_prefix_string_values(comparative_compound, "bardziej ")
        superlative_compound = deepcopy(comparative_compound)
        recursively_prefix_string_values(superlative_compound, "naj")

    lemma_object["inflections"]["simple"] = simple

    if comparative_type and int(comparative_type):
        if not adverb:
            raise Exception(f"No adverb given but comparative type is {comparative_type}.")
        lemma_object["inflections"]["adverb"] = adverb

    if comparative_type == 1:
        lemma_object["inflections"]["comparative"] = comparative_regular
        lemma_object["inflections"]["superlative"] = superlative_regular
    elif comparative_type == 2:
        lemma_object["inflections"]["comparative"] = comparative_compound
        lemma_object["inflections"]["superlative"] = superlative_compound
    elif comparative_type == 3:
        comparative_both = (comparative_compound)
        recursively_combine_string_values_into_terminus_objects(comparative_compound, comparative_regular)
        superlative_both = superlative_compound
        recursively_combine_string_values_into_terminus_objects(superlative_compound, superlative_regular)
        lemma_object["inflections"]["comparative"] = comparative_both
        lemma_object["inflections"]["superlative"] = superlative_both

    return lemma_object