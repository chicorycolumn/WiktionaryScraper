from html.parser import HTMLParser
import re

from utils.scraping.Polish_dicts import case_ref, gender_translation_ref, gender_to_tags_ref
from utils.scraping.common import orth, superstrip, add_string, brackets_to_end, trim_around_brackets, \
    split_definition_to_list


class PolishNounParser(HTMLParser):
    penultimatetag = None
    _lasttag_copy = None
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
        print("\n", "reset_for_new_table", "\n")
        self.mode = None
        print('mode = None')
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
        print("\n", "reset_for_new_table", "\n")
        self.reset_for_new_table()
        self.output_arr = []
        self.keys = []
        self.location = None
        print('location = None')

    def add_lobj_and_reset(self):
        print("\n", "add_lobj_and_reset", "\n")

        self.location = "insideword"
        print('location = "insideword"')
        self.output_obj["inflections"] = self.inflections

        self.output_obj["gender"] = gender_translation_ref[self.output_obj["gender"]]

        if self.output_obj["gender"] in gender_to_tags_ref:
            self.output_obj["tags"].extend(gender_to_tags_ref[self.output_obj["gender"]])

        if "singular" in self.output_obj["inflections"] and "plural" not in self.output_obj["inflections"]:
            self.output_obj["lacking"] = True
            self.output_obj["tantumSingulare"] = True
        elif "singular" not in self.output_obj["inflections"] and "plural" in self.output_obj["inflections"]:
            self.output_obj["lacking"] = True
            self.output_obj["tantumPlurale"] = True

        self.output_arr.append(self.output_obj)
        self.reset_for_new_table()

    def handle_data(self, data):
        data = orth(data)

        if not data or data in self.ignorable_narrow:
            return

        if self.location in ["insideselectedlang", "insideword"] \
                and self.penultimatetag in ["h1", "h2", "h3", "h4", "h5"] \
                and self.lasttag == "span" \
                and data.lower() == "noun":

            self.location = "insideword"
            print('location = "insideword"')

            self.mode = "getaspect"
            print('mode = "getaspect"')

        if self.location == "insideword":
            if self.lasttag in ["h1", "h2", "h3", "h4", "h5"] or self.penultimatetag in ["h1", "h2", "h3", "h4", "h5"]:
                split = data.split(" ")
                if split[0].lower() == "etymology" and len(split) > 1 and int(split[1]) > 1:
                    self.location = "insideselectedlang"
                    print('location = "insideselectedlang"')

        if self.location == "insideword" and self.penultimatetag in ["h1", "h2", "h3", "h4", "h5"]:
            # Mode setting from within handle_data, which is not typical.

            if self.lasttag == "span" and data.lower() == "usage notes":
                self.mode = "gettingusage"
                print('mode = "gettingusage"')

            if self.lasttag == "span" and data.lower() == "synonyms":
                self.mode = "gettingsynonyms"
                print('mode = "gettingsynonyms"')

            if data.lower() == "derived terms":
                self.mode = "getderivedterms"
                print('mode = "getderivedterms"')

        if self.location != "insidetable":
            if self.lasttag == "span" and self.penultimatetag == "h2":
                lang_in_focus = superstrip(data).lower()
                if lang_in_focus == self.selected_lang:
                    self.location = "insideselectedlang"
                    print('location = "insideselectedlang"')
                else:
                    self.location = None
                    print('location = None')

        if not self.mode:
            return

        # Adding to last output object after exiting table, which is not typical.
        if self.mode == "getderivedterms" and self.lasttag == "a" and data not in ["edit", "show ▼"]:
            self.output_arr[-1]["derivedTerms"].append(data)

        if self.mode == "gettingusage":
            self.current_usage = add_string(self.current_usage, data)

        if self.mode == "gettingsynonyms" and self.lastclass.startswith("Latn"):
            self.output_arr[-1]["synonyms"].append(data)

        if self.mode == "gettingdefinition":
            self.current_definition = add_string(self.current_definition, data)

        if self.mode.startswith("getothershapes") \
                and self.lasttag == "i" \
                and data not in ["or", ",", "/"] \
                and self.current_other_shape_key \
                and self.current_other_shape_value:
            self.output_obj["otherShapes"][self.current_other_shape_key] = self.current_other_shape_value
            self.current_other_shape_key = None
            self.current_other_shape_value = []
            self.mode = "getothershapes-key"
            print('mode = "getothershapes-key"')

        if self.mode == "getothershapes-value" and data not in self.ignorable_broad + ["(", ")"]:
            self.current_other_shape_value.append(data)

        if self.mode == "getothershapes-key":  # Not an elif.
            self.current_other_shape_key = data

        if self.mode == "getgender":
            self.output_obj["gender"] = add_string(self.output_obj["gender"], data)

        if self.mode.startswith("getword") and self.lasttag == "a":
            word_index = int(self.mode.split("-")[1])
            key = self.keys[word_index]
            subkey = self.subkey
            if subkey not in self.inflections[key]:
                self.inflections[key][subkey] = data
            else:
                if not isinstance(self.inflections[key][subkey], list):
                    self.inflections[key][subkey] = [self.inflections[key][subkey]]
                self.inflections[key][subkey].append(data)

        if self.mode == "gettingkeys":
            key_longhand = data
            self.keys.append(case_ref[key_longhand] if key_longhand in case_ref else key_longhand)

        if self.mode == "gettingsubkey":
            subkey_longhand = data
            self.subkey = case_ref[subkey_longhand] if subkey_longhand in case_ref else subkey_longhand
            self.mode = "getword-0"
            print('mode = "getword-0"')

    def handle_starttag(self, startTag, attrs):
        if startTag in ["html", "body"]:
            self.reset_for_new_word()
            return

        self.penultimatetag = self._lasttag_copy
        self._lasttag_copy = startTag
        self.lsStartTags.append(startTag)
        self.lsAll.append(startTag)

        self.currentclass = None
        for attr in attrs:
            if attr[0] == "class":
                self.currentclass = self.lastclass = attr[1]

        if self.mode == "gettingusage" and startTag in ["h1", "h2", "h3", "h4"]:
            self.output_obj["usage"].append(self.current_usage)
            self.mode = None
            print('mode = None')

        if self.mode in ["getderivedterms", "gettingsynonyms"] and startTag in ["h1", "h2", "h3", "h4"]:
            self.mode = None
            print('mode = None')

        if self.mode == "gettingdefinition" and startTag == "dd":
            self.mode = "gettingusage"
            print('mode = "gettingusage"')

        if self.mode == "getdefinitions" and startTag == "li":
            self.mode = "gettingdefinition"
            print('mode = "gettingdefinition"')

        if self.mode and self.mode.startswith("getothershapes") and startTag == "ol":
            self.mode = "getdefinitions"
            print('mode = "getdefinitions"')

        if self.mode == "getothershapes-key" and startTag == "b":
            self.mode = "getothershapes-value"
            print('mode = "getothershapes-value"')

        if self.mode == "getothershapes" and startTag == "i":
            self.mode = "getothershapes-key"
            print('mode = "getothershapes-key"')

        if self.location == "insidetable":
            if startTag == "th" and self.mode == "getsubkey":
                self.mode = "gettingsubkey"
                print('mode = "gettingsubkey"')

            if startTag == "th" and self.mode == "getkeys":
                self.mode = "gettingkeys"
                print('mode = "gettingkeys"')

            if startTag == "tr" and not self.keys:
                self.mode = "getkeys"
                print('mode = "getkeys"')

            if startTag == "table":
                self.el_count += 1

        elif self.location == "insideword":
            if startTag == "span" and self.penultimatetag == "strong":
                for attr in attrs:
                    if attr[0] == "class" and attr[1] == "gender":
                        self.mode = "getgender"
                        print('mode = "getgender"')

            elif startTag == "table":
                for attr in attrs:
                    if attr[0] == "class" and attr[1] == "wikitable inflection-table":
                        self.location = "insidetable"
                        print('location = "insidetable"')

    def handle_endtag(self, endTag):
        if self.mode == "gettingusage" and endTag == "dd":
            self.mode = "gettingdefinition"
            print('mode = "gettingdefinition"')
            self.output_obj["usage"].append(self.current_usage)
            self.current_usage = None

        if self.mode == "gettingdefinition" and endTag == "li":
            definition = brackets_to_end(trim_around_brackets(self.current_definition))
            self.output_obj["translations"]["ENG"].extend(split_definition_to_list(definition))
            self.current_definition = None
            self.mode = "getdefinitions"
            print('mode = "getdefinitions"')

        if endTag == "ol" and self.mode == "getdefinitions":
            self.mode = None
            print('mode = None')

        if self.mode and self.mode.startswith("getothershapes") and endTag == "p":
            if self.current_other_shape_key != "null" and self.current_other_shape_value:
                self.output_obj["otherShapes"][self.current_other_shape_key] = self.current_other_shape_value
            self.current_other_shape_key = None
            self.current_other_shape_value = []

        if endTag == "span" and self.mode == "getgender":
            self.mode = "getothershapes"
            print('mode = "getothershapes"')

        if endTag == "span" and self.mode and self.mode.split("-")[0] == "getword":
            word_index = int(self.mode.split("-")[1])
            self.mode = f"getword-{str(word_index + 1)}"
            print('mode = ' + f"getword-{str(word_index + 1)}")

        if endTag == "tr":
            if self.mode and self.mode.split("-")[0] == "getword":
                self.mode = "getsubkey"
                print('mode = "getsubkey"')

            elif self.mode == "gettingkeys":
                for key_longhand in self.keys:
                    key = case_ref[key_longhand] if key_longhand in case_ref else key_longhand
                    self.inflections[key] = {}
                self.mode = "getsubkey"
                print('mode = "getsubkey"')

        if endTag == "table" and self.location == "insidetable":
            if self.el_count:
                self.el_count -= 1
            else:
                self.add_lobj_and_reset()

        if self.mode != "STOP" and endTag == "body":
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

            self.mode = "STOP"
            print('mode = "STOP"')

        self.lsEndTags.append(endTag)
        self.lsAll.append(endTag)

    def handle_startendtag(self, startendTag, attrs):
        self.lsStartEndTags.append(startendTag)
        self.lsAll.append(startendTag)

    def handle_comment(self, data):
        self.lsComments.append(data)
        self.lsAll.append(data)
