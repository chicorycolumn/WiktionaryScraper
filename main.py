import html.entities
import json
from html.parser import HTMLParser
from html import entities
import urllib.request as urllib2
import urllib as urllib
from datetime import datetime
from time import sleep
import re


def parse(head_words: dict = None, use_sample: bool = False):
    parse_inflection_tables = PolishNounHTMLParser(convert_charrefs=False)

    if not head_words:
        head_words = ["małpa"]

    result = []

    for head_word in head_words:
        output_arr = None

        if use_sample:
            with open(f'output/sample_{head_word}.html', 'r') as f:
                contents = f.read()
                parse_inflection_tables.feed(contents)
                output_arr = parse_inflection_tables.output_arr
                f.close()
        else:
            html_string = html_from_head_word(head_word)
            parse_inflection_tables.feed(html_string)
            output_arr = parse_inflection_tables.output_arr
            parse_inflection_tables.output_arr = []

        if output_arr:
            print("Adding output_arr to result:", output_arr)
            for lemma_object in output_arr:
                lemma_object["lemma"] = head_word
            result.extend(output_arr)
        else:
            print(f"# No output created for {head_word}")

        if not use_sample:
            sleep(2)

    print("Writing result.")
    write_output(result)


gender_translation_ref = {
    "pl": "nonvirile",
    "m inan": "m3",
    "m anim": "m2",
    "m pers": "m1",
    "f": "f",
    "n": "n"
}


class PolishNounHTMLParser(HTMLParser):
    penultimatetag = None
    lasttag_copy = None

    lsStartTags = list()
    lsEndTags = list()
    lsStartEndTags = list()
    lsComments = list()
    lsData = list()
    lsAll = list()

    mode = None
    location = None
    output_arr = []
    selected_lang = "polish"
    ignorable_narrow = [",", "/", "(", ")"]
    ignorable_broad = ignorable_narrow + ["or", "and"]

    def reset_for_new_table(self):
        self.mode = None
        self.el_count = 0
        self.inflections = {}
        self.output_obj = {
            "lemma": None,
            "gender": None,
            "id": None,
            "translations": {"ENG": []},
            "tags": [],
            "usage": [],
            "otherShapes": {},
            "derivedTerms": [],
            "inflections": {}
        }
        self.keys = []
        self.subkey = None
        self.current_definition = None
        self.current_usage = None
        self.current_other_shape_key = None
        self.current_other_shape_value = []

    def reset_for_new_word(self):
        self.reset_for_new_table()
        self.output_arr = []
        self.keys = []

    def handle_data(self, data):
        if superstrip(data) and superstrip(data) not in ["/", ","]:

            if self.mode == "getderivedterms" and self.lasttag == "a" and orth(data) not in ["edit", "show ▼"]:
                self.output_arr[-1]["derivedTerms"].append(orth(data))

            if self.location == "insideselectedlang" and self.penultimatetag in ["h1", "h2", "h3", "h4", "h5"]:
                if orth(data) == "Derived terms":
                    self.mode = "getderivedterms"

            if self.mode == "gettingusage":
                if self.current_usage:
                    self.current_usage += f" {orth(data)}"
                else:
                    self.current_usage = orth(data)

            if self.mode == "gettingdefinition":
                if self.current_definition:
                    self.current_definition += f" {orth(data)}"
                else:
                    self.current_definition = orth(data)

            if self.mode and self.mode.startswith("getothershapes") \
                    and self.lasttag == "i" \
                    and orth(data) not in ["or", ",", "/"] \
                    and self.current_other_shape_key \
                    and self.current_other_shape_value:
                self.output_obj["otherShapes"][self.current_other_shape_key] = self.current_other_shape_value
                self.current_other_shape_key = None
                self.current_other_shape_value = []
                self.mode = "getothershapes-key"

            if self.mode == "getothershapes-value" and orth(data) and orth(data) not in self.ignorable_broad:
                self.current_other_shape_value.append(orth(data))

            if self.mode == "getothershapes-key":  # Not an elif.
                self.current_other_shape_key = orth(data)

            if self.mode == "getgender":
                if self.output_obj["gender"]:
                    self.output_obj["gender"] += f" {orth(data)}"
                else:
                    self.output_obj["gender"] = orth(data)

            if self.location != "insidetable":
                if self.lasttag == "span" and self.penultimatetag == "h2":
                    lang_in_focus = superstrip(data).lower()
                    if lang_in_focus == self.selected_lang:
                        print(f"#------------------------>ENTERING SELECTED LANG",
                              'self.location = "insideselectedlang"')
                        self.location = "insideselectedlang"
                    else:
                        self.location = None

            if self.mode and self.mode.split("-")[0] == "getword" and self.lasttag == "a":
                word_index = int(self.mode.split("-")[1])
                key = self.keys[word_index]
                subkey = self.subkey
                if subkey not in self.inflections[key]:
                    self.inflections[key][subkey] = orth(data)
                else:
                    self.inflections[key][subkey] = [self.inflections[key][subkey]]
                    self.inflections[key][subkey].append(orth(data))

            if self.mode == "gettingkeys":
                print(f"#------------------------>GETTING {orth(data)}")
                self.keys.append(orth(data))

            if self.mode == "gettingsubkey":
                print(f"#------------------------>GETTING {orth(data)}")
                self.subkey = orth(data)
                self.mode = "getword-0"

    def handle_starttag(self, startTag, attrs):

        if startTag in ["html", "body"]:
            self.reset_for_new_word()
            return

        self.penultimatetag = self.lasttag_copy
        self.lasttag_copy = startTag
        print("S TAG:", startTag)
        self.lsStartTags.append(startTag)
        self.lsAll.append(startTag)

        if self.mode == "getderivedterms" and startTag in ["h1", "h2", "h3", "h4", "h5"]:
            self.mode = None

        if self.mode == "gettingdefinition" and startTag == "dd":
            self.mode = "gettingusage"

        if self.mode == "getdefinitions" and startTag == "li":
            self.mode = "gettingdefinition"

        if self.mode and self.mode.startswith("getothershapes") and startTag == "ol":
            self.mode = "getdefinitions"

        if self.mode == "getothershapes-key" and startTag == "b":
            self.mode = "getothershapes-value"

        if self.mode == "getothershapes" and startTag == "i":
            self.mode = "getothershapes-key"

        if self.location == "insidetable":
            if startTag == "th" and self.mode == "getsubkey":
                print("#------------------------>GET SUBKEY", 'self.mode = "gettingsubkey"')
                self.mode = "gettingsubkey"

            if startTag == "th" and self.mode == "getkeys":
                print("#------------------------>GET TH", 'self.mode = "gettingkeys"')
                self.mode = "gettingkeys"

            if startTag == "tr" and not self.keys:
                print("#------------------------>ENTERING HEADER TR", 'self.mode = "getkeys"')
                self.mode = "getkeys"

            if startTag == "table":
                self.el_count += 1

        elif self.location == "insideselectedlang":
            if startTag == "span" and self.penultimatetag == "strong":
                for attr in attrs:
                    if attr[0] == "class" and attr[1] == "gender":
                        print("#------------------------>GET GENDER", 'self.mode = "getgender"')
                        self.mode = "getgender"

            elif startTag == "table":
                for attr in attrs:
                    print("attr", attr)
                    if attr[0] == "class" and attr[1] == "wikitable inflection-table":
                        print("#------------------------>ENTERING INFLECTION TABLE", 'self.location = "insidetable""')
                        self.location = "insidetable"

    def handle_endtag(self, endTag):
        if self.mode == "gettingusage" and endTag == "dd":
            self.mode = "gettingdefinition"
            self.output_obj["usage"].append(self.current_usage)
            self.current_usage = None

        if self.mode == "gettingdefinition" and endTag == "li":
            definition = brackets_to_end(trim_around_brackets(self.current_definition))
            self.output_obj["translations"]["ENG"].append(definition)
            self.current_definition = None
            self.mode = "getdefinitions"

        if endTag == "ol" and self.mode == "getdefinitions":
            self.mode = None

        if self.mode and self.mode.startswith("getothershapes") and endTag == "p":
            if self.current_other_shape_key != "null" and self.current_other_shape_value:
                self.output_obj["otherShapes"][self.current_other_shape_key] = self.current_other_shape_value
            self.current_other_shape_key = None
            self.current_other_shape_value = []

        if endTag == "span" and self.mode == "getgender":
            self.mode = "getothershapes"

        if endTag == "span" and self.mode and self.mode.split("-")[0] == "getword":
            word_index = int(self.mode.split("-")[1])
            self.mode = f"getword-{str(word_index + 1)}"

        if endTag == "tr":
            if self.mode and self.mode.split("-")[0] == "getword":
                print("#------------------------>EXITING GETWORD")
                self.mode = "getsubkey"

            elif self.mode == "gettingkeys":
                print("#------------------------>EXITING HEADER TR")
                for key in self.keys:
                    self.inflections[key] = {}
                self.mode = "getsubkey"

        if endTag == "table" and self.location == "insidetable":
            if self.el_count:
                self.el_count -= 1
            else:
                self.location = "insideselectedlang"
                self.output_obj["inflections"] = self.inflections

                self.output_obj["gender"] = gender_translation_ref[self.output_obj["gender"]]
                if self.output_obj["gender"] == "m1":
                    self.output_obj["tags"].append("person")
                elif self.output_obj["gender"] == "m2":
                    self.output_obj["tags"].append("animal")
                elif self.output_obj["gender"] == "m3":
                    self.output_obj["tags"].append("object")

                self.output_arr.append(self.output_obj)
                self.reset_for_new_table()

        print("E TAG:", endTag)
        self.lsEndTags.append(endTag)
        self.lsAll.append(endTag)

    def handle_startendtag(self, startendTag, attrs):
        print("S/E TAG:", startendTag)
        self.lsStartEndTags.append(startendTag)
        self.lsAll.append(startendTag)

    def handle_comment(self, data):
        print("COMMENT:", data)
        self.lsComments.append(data)
        self.lsAll.append(data)


def write_output(dict: dict = None):
    if not dict:
        dict = {
            "singular": {
                "nom": "ma\\xc5\\x82pa",
                "acc": "ma\\xc5\\x82p\\xc4\\x99"
            },
        }

    json_object = json.dumps(dict, indent=4, ensure_ascii=False)

    with open("output/output.json", "w") as outfile:
        outfile.write(json_object)


def html_from_head_word(head_word):
    print(datetime.now().strftime('%H:%M:%S'), f"{head_word} is being loaded up as a Wiktionary page.")
    html_page = urllib2.urlopen(f"https://en.wiktionary.org/wiki/{urllib.parse.quote(head_word)}")
    return str(html_page.read())


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
    return str.encode('utf-8').decode('unicode-escape').encode('iso-8859-1').decode('utf-8')
    # source: https://stackoverflow.com/a/49756591
    # 1. actually any encoding support printable ASCII would work, for example utf-8
    # 2. unescape the string, see https://stackoverflow.com/a/1885197
    # 3. latin-1 also works, see https://stackoverflow.com/q/7048745
    # 4. finally decode again


if __name__ == '__main__':
    # Sample ser has meanings in many languages, but we only want the Polish one.
    # Sample rok has that too, but also, it has two inflection tables in Polish, and we want both.
    # Sample baba has multiple other shapes.
    parse(["miesiąc", "rok", "małpa"])
    # write_output()
