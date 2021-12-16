from utils.postprocessing.common import recursively_minimise
from utils.general.common import recursively_replace_keys_in_dict, recursively_count_strings, write_todo

import copy


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
            write_todo(f'SKIPPED. Lobj "{lemma_object["lemma"]}" has unexpected aspect: "{lemma_object["aspect"]}".')
            return

        for py_key, js_key_and_count in tense_ref.items():
            js_key = js_key_and_count[0]
            if js_key == "future":
                print("")
            expected_count = js_key_and_count[1]
            actual_count = recursively_count_strings(full_inflections[py_key])
            if actual_count != expected_count:
                if actual_count + 5 == expected_count:
                    write_todo(f'The "{js_key}" tense on "{lemma_object["lemma"]}" should have {expected_count} strings but has {actual_count}. I think the Wiktionary page was missing the "{js_key} impersonal", but nevertheless the word does have it, so I have gone ahead and minimised the "{js_key} impersonal" to True boolean. If you disagree, you must change that.')
                else:
                    write_todo(f'SKIPPED. "{js_key}" tense on "{lemma_object["lemma"]}" should have {expected_count} strings but has {actual_count}.')
                    return

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
