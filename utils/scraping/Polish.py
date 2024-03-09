from utils.postprocessing.common import recursively_minimise
from utils.general.common import recursively_replace_keys_in_dict, recursively_count_strings, write_todo

import copy


def minimise_inflections(lemma_object):
    print("START minimise_inflections", lemma_object["lemma"])

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
        "1 st": "1per",
        "2 nd": "2per",
        "3 rd": "3per",
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

    def lower_bound_message_function(js_key, lemma_object, expected_count, actual_count):
        return f'The "{js_key}" tense on {lemma_object["aspect"]} ' \
        f'"{lemma_object["lemma"]}" should have {expected_count} ' \
        f'strings but has {actual_count}. I think the Wiktionary ' \
        f'page was missing the "{js_key} impersonal", I have ' \
        f'gone ahead and minimised the "{js_key}" to True boolean. ' \
        f'If you disagree, you must change that.'

    def upper_bound_message_function_future(js_key, lemma_object, expected_count, actual_count):
        return f'The "{js_key}" tense on {lemma_object["aspect"]} ' \
        f'"{lemma_object["lemma"]}" should have {expected_count} ' \
        f'strings but has {actual_count}.'

    def upper_bound_message_function_conditional(js_key, lemma_object, expected_count, actual_count):
        return f'The "{js_key}" tense on {lemma_object["aspect"]} ' \
        f'"{lemma_object["lemma"]}" should have {expected_count} ' \
        f'strings but has {actual_count}. Wiktionary now includes "bym chodził" ' \
        f'as well as "chodziłbym" so number is doubled.'

    if lemma_object["lemma"] != "być":
        if lemma_object["aspect"] == "imperfective":
            tense_count_acceptable_bounds_ref = {
                "future": {
                    "js_key": "future",
                    "expected_count": {"value": 31, "message": None},
                    "lower_bound": {"value": 26, "message": lower_bound_message_function},
                    "upper_bound": {"value": 26, "message": upper_bound_message_function_future},
                },
                "conditional": {
                    "js_key": "conditional",
                    "expected_count": {"value": 18, "message": None},
                    "lower_bound": {"value": 13, "message": lower_bound_message_function},
                    "upper_bound": {"value": 31, "message": upper_bound_message_function_conditional},
                }
            }
        elif lemma_object["aspect"] == "perfective":
            tense_count_acceptable_bounds_ref = {
                "conditional": {
                    "js_key": "conditional",
                    "expected_count": {"value": 18, "message": None},
                    "lower_bound": {"value": 13, "message": lower_bound_message_function},
                    "upper_bound": {"value": 31, "message": upper_bound_message_function_conditional},
                }
            }
        else:
            msg = f'SKIPPED this whole lobj in minimise_inflections. Lobj "{lemma_object["lemma"]}" has unexpected aspect: "{lemma_object["aspect"]}".'
            write_todo(msg, True)
            return

        for py_key, acceptable_bounds_dict in tense_count_acceptable_bounds_ref.items():
            js_key = acceptable_bounds_dict["js_key"]

            actual_count = recursively_count_strings(full_inflections[py_key])
            expected_count = acceptable_bounds_dict["expected_count"]["value"]

            if actual_count != expected_count:
                if actual_count == acceptable_bounds_dict["lower_bound"]["value"]:
                    msg = acceptable_bounds_dict["lower_bound"]["message"](js_key, lemma_object, expected_count, actual_count)
                    write_todo(msg, True)
                elif actual_count == acceptable_bounds_dict["upper_bound"]["value"]:
                    msg = acceptable_bounds_dict["upper_bound"]["message"](js_key, lemma_object, expected_count, actual_count)
                    write_todo(msg, True)
                else:
                    msg = f'SKIPPED this entire lobj in minimise_inflections. "{js_key}" tense on {lemma_object["aspect"]} "{lemma_object["lemma"]}" should have {expected_count} strings but has {actual_count} and does not match upper or lower bound.'
                    write_todo(msg, True)
                    return

            full_inflections[js_key] = True
            if py_key != js_key:
                full_inflections.pop(py_key)

    # STEP THREE
    #       Minimise, eg where "m", "f", "n" keys all hold same value, minimise to just "allSingularGenders" key.

    recursively_minimise(full_inflections, {
        "_SingularGenders": ["m", "f", "n"],
        "_SingularGendersExcludingNeuter": ["m", "f"],
        "_PluralGenders": ["virile", "nonvirile"]
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
