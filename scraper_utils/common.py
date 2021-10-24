import json
import urllib.request as urllib2
import urllib as urllib
from datetime import datetime
import re

minimised_gender_key_ref_polish = {
    "masculine": "m",
    "feminine": "f",
    "neuter": "n"
}


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
    print("### key_ref", key_ref)
    for key, value in dic.items():
        print("}}}}", key)
        if key in key_ref:
            print(">", key)
            dic[key_ref[key]] = value
            print(f"## Replaced {key} with {key_ref[key]}")
            dic.pop(key)
        if type(value) is dict:
            print(">>", key)
            recursively_replace_keys_in_dict(value, key_ref)


def get_base_id(id):
    return re.search("^\d+\.\d+", str(id)).group()


def write_output(dict: dict = {}, output_file: str = "output", folder: str = "output", full_output_path: str = None):
    json_object = json.dumps(dict, indent=4, ensure_ascii=False)

    if not full_output_path:
        full_output_path = f"{folder}/{output_file}.json"

    with open(full_output_path, "w") as outfile:
        outfile.write(json_object)


def html_from_head_word(head_word, log_string):
    print(f'\n# Loading word [{log_string}] at <<{datetime.now().strftime("%H:%M:%S")}>> as Wiktionary page for "{head_word}".\n')
    html_page = urllib2.urlopen(f"https://en.wiktionary.org/wiki/{urllib.parse.quote(head_word)}")
    return str(html_page.read())


def add_string(locus, string):
    return f"{locus} {string}" if locus else string


def split_definition_to_list(str):
    match = re.match(r"(?P<nonbracketed>^.+?)\s(?P<bracketed>\(.+)", str)
    return [match["nonbracketed"], match["bracketed"]] if match else [str]


def brackets_to_end(s):
    return re.sub(r"(?P<bracketed>\(.+\))\s(?P<nonbracketed>.+$)", r"\g<nonbracketed> \g<bracketed>", s)


def trim_around_brackets(str):
    str = re.sub(r"\(\s(\w)", "(\g<1>", str)
    str = re.sub(r"(\w)\s\)", "\g<1>)", str)
    str = re.sub(r"(\w)\s,", "\g<1>,", str)
    return str


def orth(str):
    return double_decode(superstrip(str))


def superstrip(str):
    return str.replace("\\n", "").strip()


def double_decode(str):
    str = re.sub(r"\s\s", "", str)
    a = str.encode('utf-8')
    b = a.decode('unicode-escape')
    c = b.encode('iso-8859-1')
    d = c.decode('utf-8', errors="replace")
    return d
    # source: https://stackoverflow.com/a/49756591
    # 1. actually any encoding support printable ASCII would work, for example utf-8
    # 2. unescape the string, see https://stackoverflow.com/a/1885197
    # 3. latin-1 also works, see https://stackoverflow.com/q/7048745
    # 4. finally decode again
