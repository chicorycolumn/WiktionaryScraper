from utils.general.common import write_todo, write_output, get_value_from_keypath, get_base_temp_id
from input.Polish.nouns.head_words import person_nouns_without_m1_gender

import copy
import json
import re
import os
from utils.scraping.Polish_dicts import shorthand_tag_refs

def make_ids(langcode, wordtype, group_number="None", lemma_objects=None, existing_lemma_objects_path=None, is_first_time=False):
    if not existing_lemma_objects_path:
        existing_lemma_objects_path = f'output_saved/{wordtype}'
    existing_lemma_objects = []
    for root, dirs, files in os.walk(existing_lemma_objects_path):
        for file in files:
            print(file)
            with open(f'{existing_lemma_objects_path}/{file}', "r") as f:
                loaded = json.load(f)
                existing_lemma_objects.extend(loaded)
                f.close()

    if not is_first_time:
        existing_lemmas = []
        passing_lemmas = []
        for lemma_object in lemma_objects:
            if any(elobj["lemma"] == lemma_object["lemma"] for elobj in existing_lemma_objects):
                existing_lemmas.append(lemma_object["lemma"])
            else:
                passing_lemmas.append(lemma_object)
        if existing_lemmas:
            print("LIST I THINK ARE DUPLICATES. I did not create IDs for these lObjs:")
            for lemma in existing_lemmas:
                print(lemma)
                write_todo(f'Group {group_number} lObj "{lemma}" I believe already done. Removed from this output.')
            print("/LIST")
        lemma_objects = passing_lemmas

    res_arr = []

    if wordtype == "nouns":
        for lemma_object in lemma_objects:
            if lemma_object["lemma"][0] == lemma_object["lemma"][0].upper():
                lemma_object["isProperNoun"] = True

    id_number_counts = {
        "nco": 0,
        "npe": 0,
        "ver": 0,
        "adj": 0,
    }
    for elobj in existing_lemma_objects:
        split = elobj["id"].split("-")
        lang = split[0]
        wordtypeshortcode = split[1]
        number = split[2]
        if lang != "pol":
            raise Exception("220")
        if int(number) > id_number_counts[wordtypeshortcode]:
            id_number_counts[wordtypeshortcode] = int(number)

    for lemma_object in lemma_objects:
        if wordtype == "adjectives":
            wordtypeshortcode = "adj"
        elif wordtype == "verbs":
            wordtypeshortcode = "ver"
        elif wordtype == "nouns":
            wordtypeshortcode = "npe" \
                if lemma_object["gender"] == "m1" or lemma_object["lemma"] in person_nouns_without_m1_gender \
                else "nco"

        sibling_info = []
        number = id_number_counts[wordtypeshortcode] + 1
        number = "{0:03}".format(number)

        iterations = [[existing_lemma_objects, True], [res_arr, False]]

        # Give lobjs same id number if they are otherShapes of each other.
        for iteration in iterations:
            existing_or_result_lemma_objects = iteration[0]
            is_existing = iteration[1]

            for elobj in existing_or_result_lemma_objects:
                if not sibling_info and "otherShapes" in elobj:
                    for shape_key, shape_values in elobj["otherShapes"].items():
                        if lemma_object["lemma"] in shape_values:
                            sibling_info.append(shape_key[0:4])
                            number = elobj["id"].split("-")[2]
                            if "(" not in elobj["id"].split("-")[3]:
                                parent_info = "?"
                                if "otherShapes" in lemma_object:
                                    for sh_key, sh_values in lemma_object["otherShapes"].items():
                                        if elobj["lemma"] in sh_values:
                                            parent_info = sh_key
                                if is_existing or len(parent_info) == 1:
                                    write_todo(
                                        f'Manually add sibling_info "{parent_info[0:4]}" to id of "{elobj["id"]}".')
                                else:
                                    elobj["id"] += f'({parent_info[0:4]})'

        if sibling_info:
            sibling_info = [sibling_info[0]]

        # Give lobjs sibling info if are same lemma but don't give same number.
        for iteration in iterations:
            existing_or_result_lemma_objects = iteration[0]
            is_existing = iteration[1]
            for elobj in existing_or_result_lemma_objects:
                if elobj["lemma"] == lemma_object["lemma"]:

                    first_translation = lemma_object["translations"]["ENG"][0]
                    sibling_info_datum = first_translation if wordtype != "verbs" \
                        else re.match(r".+?to\s(?P<bare_infinitive>.+?)\s", first_translation)["bare_infinitive"]

                    sibling_info.append(sibling_info_datum)

                    if "(" not in elobj["id"].split("-")[3]:
                        first_translation = elobj["translations"]["ENG"][0]
                        parent_info_datum = first_translation if wordtype != "verbs" \
                            else re.match(r".+?to\s(?P<bare_infinitive>.+?)\s", first_translation)["bare_infinitive"]

                        if is_existing:
                            write_todo(f'To "{elobj["id"]}" ID must append "{parent_info_datum}"')
                        else:
                            elobj["id"] += f'({parent_info_datum})'

        if int(number) == id_number_counts[wordtypeshortcode] + 1:
            id_number_counts[wordtypeshortcode] += 1

        sibling_info = f'({",".join(sibling_info)})' if sibling_info else ""
        id = f'{langcode}-{wordtypeshortcode}-{number}-{lemma_object["lemma"]}{sibling_info}'
        lemma_object["id"] = id
        lemma_object.pop("temp_id")
        res_arr.append(lemma_object)

    return res_arr


def recursively_combine_string_values_into_terminus_objects(dict1, dict2):
    keypath = []

    for key, value in dict1.items():
        keypath.append(key)

        if type(value) in [str, list] or (type(value) is dict and "isTerminus" in value and value["isTerminus"]):
            normal = []
            additionalInfrequent = []

            if type(value) == str:
                normal = [value]
            elif type(value) == list:
                normal = value[:]
            elif type(value) == dict:
                normal = value["normal"][:]
                additionalInfrequent = value["additionalInfrequent"][:] if "additionalInfrequent" in value else []

            dict2_value = get_value_from_keypath(dict2, keypath)

            if type(dict2_value) == str:
                normal.append(dict2_value)
                normal.reverse()
            elif type(dict2_value) == list:
                normal.extend(dict2_value)
                normal.reverse()
            elif type(dict2_value) == dict and "isTerminus" in dict2_value and dict2_value["isTerminus"]:
                normal.extend(dict2_value["normal"] if "normal" in dict2_value else [])
                additionalInfrequent.extend(dict2_value["additionalInfrequent"] if "additionalInfrequent" in dict2_value else [])
            else:
                raise Exception(f"Unexpected type {type(dict2_value)} at keypath {keypath}.")

            terminus_object = {
                "isTerminus": True,
                "normal": normal,
            }

            if additionalInfrequent:
                terminus_object["additionalInfrequent"] = additionalInfrequent

            get_value_from_keypath(dict1, keypath[:-1])[key] = terminus_object




        elif type(value) == dict:
            recursively_combine_string_values_into_terminus_objects(value, get_value_from_keypath(dict2, keypath))
        else:
            raise Exception(f"Unexpected type {type(value)} of {value} at keypath {keypath}.")

        keypath.pop()


def recursively_expand_tags(input_stags: list, ref: object):
    output_tags = []

    def ret_inner(input_tags: list):
        for tag in input_tags:
            if tag in ref:
                ret_inner(ref[tag]["tags"])
            elif tag not in output_tags:
                output_tags.append(tag)

    ret_inner(input_stags)
    return output_tags


def add_tags_and_topics_from_shorthand(lemma_object: object, ref: object):
    shorthand_tags = lemma_object["tags"].split(",")

    tags = recursively_expand_tags(shorthand_tags, ref)

    topics = []
    for stag in shorthand_tags:
        if stag in ref:
            for topic in ref[stag]["topics"]:
                if topic not in topics:
                    topics.append(topic)

    tags.sort()
    topics.sort()

    lemma_object["tags"] = tags
    lemma_object["topics"] = topics


def untruncate_lemma_objects(group_number, wordtype):
    res_arr = []

    with open(f"output_saved/output_{wordtype}_{group_number}.json", "r") as f:
        lobjs_long = json.load(f)
        f.close()
    with open(f"output_saved/truncated_{wordtype}_{group_number}.json", "r") as f:
        lobjs_truncated = json.load(f)
        f.close()

    for lemma_object in lobjs_truncated:
        lemma_object_long = [lol for lol in lobjs_long if lol["temp_id"] == get_base_temp_id(lemma_object["temp_id"])][
            0]

        for key in lemma_object_long:
            if key not in lemma_object:
                lemma_object[key] = lemma_object_long[key]

        res_arr.append(lemma_object)

    write_output(res_arr, f"untruncated_{wordtype}_{group_number}", f"output_saved")


def recursively_minimise(dic, ref):
    def rm_inner(dic):
        for combined_key, keys in ref.items():
            if keys[0] in dic and all(key in dic for key in keys):
                # This dic contains all keys of this arr, eg [m, f, n], so it let's replace with "allSingularGenders"
                # provided of course, they all contain same value.
                values = [json.dumps(dic[key]) for key in keys]
                if all(v == values[0] for v in values[1:]):
                    # They all contain the same value, eg at keys "m", "f", and "n".
                    dic[combined_key] = copy.deepcopy(dic[keys[0]])
                    for key in keys:
                        dic.pop(key)
                    return
        for k, v in dic.items():
            if type(v) is dict:
                rm_inner(v)

    rm_inner(dic)


def recursively_prefix_string_values(obj, prefix):
    for key, value in obj.items() if type(obj) is dict else enumerate(obj):
        if type(value) == str:
            obj[key] = f"{prefix}{value}"
        elif type(value) in [dict, list]:
            recursively_prefix_string_values(value, prefix)


def expand_tags_and_topics(group_number, wordtype):
    res_arr = []

    with open(f"output_saved/untruncated_{wordtype}_{group_number}.json", "r") as f:
        untruncated_lobjs = json.load(f)
        f.close()

    for lemma_object in untruncated_lobjs:
        add_tags_and_topics_from_shorthand(lemma_object, shorthand_tag_refs)
        res_arr.append(lemma_object)

    return res_arr


def finalise_lemma_objects(group_number, wordtype, langcode, skip_make_ids=False, is_first_time=False):
    untruncate_lemma_objects(group_number, wordtype)
    res_arr = expand_tags_and_topics(group_number, wordtype)
    if not skip_make_ids:
        res_arr = make_ids(langcode=langcode, wordtype=wordtype, lemma_objects=res_arr, is_first_time=is_first_time, group_number=group_number)
    write_output(res_arr, f"finished_{wordtype}_{group_number}", f"output_saved/{wordtype}")