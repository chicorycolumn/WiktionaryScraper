import copy
import json
from datetime import datetime
import re
import os


def get_existing_lobjs(wordtype: str, lemmas_only: bool = False, existing_lobjs_path: str = None):
    if not existing_lobjs_path:
        existing_lobjs_path = f'output_saved/{wordtype}'

    existing_lemma_objects = []
    for root, dirs, files in os.walk(existing_lobjs_path):
        for file in files:
            with open(f'{existing_lobjs_path}/{file}', "r") as f:
                loaded = json.load(f)
                existing_lemma_objects.extend(loaded)
                f.close()

    if lemmas_only:
        return [lobj["lemma"] for lobj in existing_lemma_objects]

    return existing_lemma_objects


def get_rejected_lobjs(wordtype: str):
    existing_lobjs_path = f'output_saved/rejected'

    rejected_lemmas = []
    for root, dirs, files in os.walk(existing_lobjs_path):
        for file in files:
            if wordtype in file.split("_"):
                with open(f'{existing_lobjs_path}/{file}', "r") as f:
                    loaded = json.load(f)
                    for k in loaded:
                        if k != "already_existing":
                            print(4421, file, len(loaded[k]), k, loaded[k])
                            rejected_lemmas.extend(loaded[k])
                    f.close()

    return rejected_lemmas


def get_value_from_keypath(dict, keypath):
    for key in keypath:
        dict = dict[key]
    return dict


def write_todo(msg):
    with open("TODO.txt", "a") as f:
        f.write(
            "\n"
            + str(datetime.now())[:-10]
            + " "
            + msg
        )
        f.close()


def recursively_count_strings(obj):
    strings = []

    def rcs_inner(obj):
        for key, value in obj.items() if type(obj) is dict else enumerate(obj):
            if type(value) in [dict, list]:
                rcs_inner(value)
            elif type(value) is str:
                strings.append(value)

    rcs_inner(obj)
    return len(strings)


def recursively_replace_keys_in_dict(dic, key_ref):
    def rrkid_inner(dic, key_ref):
        for key in copy.deepcopy(dic):
            value = dic[key]
            if key in key_ref:
                dic[key_ref[key]] = value
                dic.pop(key)
            if type(value) is dict:
                rrkid_inner(value, key_ref)

    rrkid_inner(dic, key_ref)


def get_base_temp_id(id):
    return re.search("^\d+\.\d+", str(id)).group()


def write_output(dict: dict = {}, output_file: str = "output", folder: str = "output", full_output_path: str = None):
    if not os.path.isdir(folder):
        os.mkdir(folder)

    json_object = json.dumps(dict, indent=4, ensure_ascii=False)

    if not full_output_path:
        full_output_path = f"{folder}/{output_file}.json"

    with open(full_output_path, "w") as outfile:
        outfile.write(json_object)
