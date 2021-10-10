def generate_adjective(lemma: str, translations_list: list, comparative_type: int, pluvirnom_lemma, adverb: str = None, comparative: str = None):
    def recursively_prefix_string_values(dict, prefix):
        for key, value in dict.items():
            if type(value) == str:
                dict[key] = f"{prefix}{value}"
            else:
                recursively_prefix_string_values(value)

    lemma_mod_1 = lemma[0:-1] if lemma[-1] == "y" else lemma
    lemma_mod_2 = lemma[0:-1]

    lemma_object = {
        "translations": {"ENG": translations_list},
        "tags": "xxxxxxxx",

        "lemma": lemma,
        "id": None,

        "inflections": {
            "adverb": adverb,
            "simple": {
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
        }
    }

    if comparative_type in [1, 3]:
        com_mod_1 = comparative[0:-1]
        pluvirnom_com = comparative[0:-2] + "i"
        comparative_inflections = {
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

        if comparative == 3:
            recursively_prefix_string_values()


    # narodowy  Type 0  is NOT COMPARABLE
    # stary     Type 1  has REGULAR comparative/superlative (starszy and najstarszy)
    # żółty     Type 2  has COMPOUND comparative/superlative (bardziej żółty and najbardziej żółty)
    # czerwony  Type 3  has BOTH REGULAR AND COMPOUND comparative/superlative
