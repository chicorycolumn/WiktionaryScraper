import urllib.request as urllib2
import urllib as urllib
from datetime import datetime
import re


def format_verb_translation_properties(s):
    ref = {
        "reflexive": "r",
        "intransitive": "i",
        "transitive": "t",
        "pronominal": "pr",
        "reciprocal": "rc",
        "passive": "pa",
    }

    bracketed_parts = re.findall(r"\(.+?\)", s)
    properties_string = None
    if bracketed_parts:
        for bracketed_part in bracketed_parts:
            bracketed_part_strings = bracketed_part[1:-1].split(" ")
            if any(bracketed_part_string in ref for bracketed_part_string in bracketed_part_strings):
                properties_string = bracketed_part
                properties_formatted_arr = []
                for bracketed_part_string in bracketed_part_strings:
                    if bracketed_part_string in ref:
                        properties_formatted_arr.append(ref[bracketed_part_string])
                    else:
                        properties_formatted_arr.append(bracketed_part_string)
                properties_formatted_str = f'[{",".join(properties_formatted_arr)}]'

    infinitive = re.match(r".+?[\(]", s).group()[0:-1].strip() if "(" in s else s.strip()

    if properties_string:
        if properties_formatted_str == "[t]":
            properties_formatted_str = ""
        s = s.replace(properties_string, "").replace(infinitive, f'{infinitive}{properties_formatted_str}')

    return s.strip()


def format_brackets_for_translation_strings(input):
    res = []
    in_parentheses = False
    parenthetical_strings = []
    for str in input:
        if not re.match(r"[()a-zA-Z0-9]+", str):
            continue
        if str == "(":
            in_parentheses = True
        elif str == ")":
            in_parentheses = False
            res.append(f"({' '.join(parenthetical_strings)})")
            parenthetical_strings = []
        elif in_parentheses:
            parenthetical_strings.append(str)
        else:
            res.append(str)
    return res


def process_extra(output_obj):
    if output_obj["extra"]["usage"]:

        adjusted_usage_arr = []
        for str in output_obj["extra"]["usage"]:
            mat = re.match(r".+(Antonym|Synonym).+", str)
            match = re.search(r"(?P<first_bit>.+)(?P<second_bit>(Antonym|Synonym).+)", str)

            if mat:
                adjusted_usage_arr.extend([match["first_bit"].strip(), match["second_bit"].strip()])
            else:
                adjusted_usage_arr.append(str.strip())
        output_obj["extra"]["usage"] = adjusted_usage_arr

        usages_copy = output_obj["extra"]["usage"][:]
        for item in usages_copy:
            cease = False
            for string in [
                "Synonyms: see Thesaurus:",
                "Synonym: see Thesaurus:",
                "Synonyms:",
                "Synonym:",
            ]:
                if not cease and item.startswith(string):
                    match = re.match(fr"(?P<drop_this>{string}) (?P<keep_this>.+)", item)
                    print("Move this from Usage to Synonyms:", match["keep_this"])
                    output_obj["extra"]["synonyms"].append(match["keep_this"])
                    output_obj["extra"]["usage"].remove(item)
                    cease = True

        for item in usages_copy:
            cease = False
            for string in [
                "Antonyms: see Thesaurus:",
                "Antonym: see Thesaurus:",
                "Antonyms:",
                "Antonym:",
            ]:
                if not cease and item.startswith(string):
                    match = re.match(fr"(?P<drop_this>{string}) (?P<keep_this>.+)", item)
                    print("Move this from Usage to Antonyms:", match["keep_this"])
                    output_obj["extra"]["antonyms"].append(match["keep_this"])
                    output_obj["extra"]["usage"].remove(item)
                    cease = True

    for key in ["usage", "otherShapes", "derivedTerms", "synonyms", "antonyms"]:
        if not output_obj["extra"][key]:
            output_obj["extra"].pop(key)
        elif type(output_obj["extra"][key]) is list:
            arr = []
            for str in output_obj["extra"][key]:
                if str not in arr:
                    arr.append(str)
            output_obj["extra"][key] = arr

            arr = []
            if key not in ["usage", "derivedTerms"]:
                for el in output_obj["extra"][key]:
                    arr.extend(el.split(" "))
                output_obj["extra"][key] = arr

    if not output_obj["extra"]:
        output_obj.pop("extra")

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


def html_from_head_word(head_word, head_word_index, len_head_words):
    print(f'\n# Loading Wiktionary "{head_word_index + 1} of {len_head_words}" at <<{datetime.now().strftime("%H:%M:%S")}>> for "{head_word}".\n')
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
