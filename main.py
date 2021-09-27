from scraper_utils.common import *
from scraper_utils.Polish import gender_translation_ref as gender_translation_ref_polish
from html.parser import HTMLParser
import re


class PolishNounHTMLParser(HTMLParser):
    penultimatetag = None
    lasttag_copy = None
    currentclass = None
    lastclass = None

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

    ignorable_narrow = [",", "/", ";"]
    ignorable_broad = ignorable_narrow + ["or", "and"]

    def reset_for_new_table(self):
        self.mode = None
        self.el_count = 0
        self.inflections = {}
        self.output_obj = {
            "lemma": None,
            "gender": None,
            "tags": [],
            "translations": {"ENG": []},
            "id": None,
            "usage": [],
            "otherShapes": {},
            "derivedTerms": [],
            "synonyms": [],
            "inflections": {},
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
        if superstrip(data) and superstrip(data) not in self.ignorable_narrow:

            # Mode setting from within handle_data, which is not typical.
            if self.location == "insidecurrentlanguage":
                if self.lasttag == "span" and self.penultimatetag in ["h1", "h2", "h3", "h4", "h5"] and orth(
                        data).lower() == "usage notes":
                    self.mode = "gettingusage"

                if self.lasttag == "span" and self.penultimatetag in ["h1", "h2", "h3", "h4", "h5"] and orth(
                        data).lower() == "synonyms":
                    self.mode = "gettingsynonyms"

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

            if self.mode == "gettingsynonyms" and self.lastclass == "Latn" and orth(data):
                self.output_arr[-1]["synonyms"].append(orth(data))

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

            if self.mode == "getothershapes-value" and orth(data) and orth(data) not in self.ignorable_broad + ["(",
                                                                                                                ")"]:
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

        self.currentclass = None
        for attr in attrs:
            if attr[0] == "class":
                self.currentclass = self.lastclass = attr[1]

        if self.mode == "gettingusage" and startTag in ["h1", "h2", "h3", "h4"]:
            self.output_obj["usage"].append(self.current_usage)
            self.mode = None

        if self.mode in ["getderivedterms", "gettingsynonyms"] and startTag in ["h1", "h2", "h3", "h4"]:
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
            self.output_obj["translations"]["ENG"].extend(split_definition_to_list(definition))
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

                self.output_obj["gender"] = gender_translation_ref_polish[self.output_obj["gender"]]
                if self.output_obj["gender"] == "m1":
                    self.output_obj["tags"].append("person")
                elif self.output_obj["gender"] == "m2":
                    self.output_obj["tags"].append("animal")
                elif self.output_obj["gender"] == "m3":
                    self.output_obj["tags"].append("inanimate")

                if "singular" in self.output_obj["inflections"] and "plural" not in self.output_obj["inflections"]:
                    self.output_obj["lacking"] = True
                    self.output_obj["tantumSingulare"] = True
                elif "singular" not in self.output_obj["inflections"] and "plural" in self.output_obj["inflections"]:
                    self.output_obj["lacking"] = True
                    self.output_obj["tantumPlurale"] = True

                self.output_arr.append(self.output_obj)
                self.reset_for_new_table()

        if endTag == "body":
            for output_obj in self.output_arr:
                if output_obj["usage"]:
                    usages_copy = output_obj["usage"][:]
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
                                output_obj["synonyms"].append(match["keep_this"])
                                output_obj["usage"].remove(item)
                                cease = True

                for key in ["usage", "otherShapes", "derivedTerms", "synonyms"]:
                    if not output_obj[key]:
                        output_obj.pop(key)

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


if __name__ == '__main__':
    # Sample ser has meanings in many languages, but we only want the Polish one.
    # Sample rok has that too, but also, it has two inflection tables in Polish, and we want both.
    # Sample baba has multiple other shapes.
    # parse(["dzień", "ręka", "brak"])
    scrape_word_data(
        "Polish",
        PolishNounHTMLParser(convert_charrefs=False),
        # ["prysznic", "glista", "gleba", "łeb", "BADWORD", "palec", "noga", "piła", "piłka"],
        # False
        ["baba", "bałagan", "cel", "drzwi", "dzień", "małpa", "miesiąc", "rok", "ser"],
        True
    )
    # write_output()
