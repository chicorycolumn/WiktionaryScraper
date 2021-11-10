import copy
import json
from datetime import datetime
import re
import os


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
                recursively_replace_keys_in_dict(value, key_ref) #swde use inner fxn instead

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