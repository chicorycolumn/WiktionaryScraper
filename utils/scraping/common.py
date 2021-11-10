import urllib.request as urllib2
import urllib as urllib
from datetime import datetime
import re


def add_value_at_keychain(value, keychain, dict):
    for index, key in enumerate(keychain):
        if key not in dict:
            dict[key] = {}
        if index + 1 == len(keychain):
            dict[key] = value
        else:
            dict = dict[key]


def trim_chaff_from_derived_terms(string, lemma):
    strings_to_cut = [
        f"[ edit ] show ▼ verbs derived from {lemma}",
        "[ edit ] show ▼ ",
        "related terms [ edit ]",
        "[ edit ] ",
        f"verbs derived from {lemma} "
    ]
    for to_cut in strings_to_cut:
        if to_cut in string.lower():
            string = string.lower().replace(to_cut, "")
            if string.startswith(" "):
                string = string[1:]
    return string


def html_from_head_word(head_word, log_string):
    print(f'\n# Loading Wiktionary "{log_string}" at <<{datetime.now().strftime("%H:%M:%S")}>> for "{head_word}".\n')
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