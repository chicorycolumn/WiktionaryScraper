from scraper_utils.common import *
from scraper_utils.Polish import *
from html.parser import HTMLParser
import re

"""
Do the language heading detection as normal.

When you get to a h3 then span with class mw-headline and value "Adjective", CHANGE MODE TO GETCOMP

i with value "comparative", then collect all values and join with space, that's the comparative.

i with value "superlative", do the same.

i with value "adverb", do the same, and stop when end tag is p.

You will also use these to work out the comparativeType.

NOW CHANGE MODE TO GETTRANS

You enter an ol. Gather all values into translations arr until you exit ol.

Now get the ultimate value of the 4th td inside the 3rd tr, that's the pluvirnom.

And that's it!
"""


class PolishAdjectiveParser(HTMLParser):
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

    tr_count = 0
    td_count = 0

    def reset_for_new_table(self):
        self.mode = None
        self.el_count = 0
        self.inflections = {}
        self.output_obj = {
            "lemma": [],
            "translations": [],
            "comparative_type": None,
            "pluvirnom": [],
            "adverb": [],
            "comparative": []
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
        self.location = None

    def handle_data(self, data):
        data = orth(data)

        if not data or data in self.ignorable_narrow + ["(", ")"]:
            return

        if self.location == "insideselectedlang":
            if self.mode == "gettingpluvirnom":
                self.output_obj["pluvirnom"].append(data)

            if self.mode == "gettinglemma":
                self.output_obj["lemma"].append(data)

            if self.mode == "gettingtranslations":
                self.output_obj["translations"].append(data)

            if self.mode == "gettingadverb":
                self.output_obj["adverb"].append(data)

            if self.lasttag == "i" and data.lower() == "adverb":
                self.mode = "gettingadverb"

            if self.lasttag == "i" and data.lower() == "superlative":
                self.mode = None

            if self.mode == "gettingcomparative":
                self.output_obj["comparative"].append(data)

            if self.lasttag == "i" and data.lower() == "comparative":
                self.mode = "gettingcomparative"

        if self.penultimatetag in ["h1", "h2", "h3", "h4", "h5"]:
            if self.location == "insideselectedlang":
                if self.lasttag == "span" and data.lower() == "adjective":
                    self.mode = "getcomparativeinfo"
            elif data.lower() == self.selected_lang:
                self.location = "insideselectedlang"

        # if not self.mode:
        #     return
        #
        # # Adding to last output object after exiting table, which is not typical.
        # if self.mode == "getderivedterms" and self.lasttag == "a" and data not in ["edit", "show ▼"]:
        #     self.output_arr[-1]["derivedTerms"].append(data)
        #
        # if self.mode == "gettingusage":
        #     self.current_usage = add_string(self.current_usage, data)
        #
        # if self.mode == "gettingsynonyms" and self.lastclass.startswith("Latn"):
        #     self.output_arr[-1]["synonyms"].append(data)
        #
        # if self.mode == "gettingdefinition":
        #     self.current_definition = add_string(self.current_definition, data)
        #
        # if self.mode.startswith("getothershapes") \
        #         and self.lasttag == "i" \
        #         and data not in ["or", ",", "/"] \
        #         and self.current_other_shape_key \
        #         and self.current_other_shape_value:
        #     self.output_obj["otherShapes"][self.current_other_shape_key] = self.current_other_shape_value
        #     self.current_other_shape_key = None
        #     self.current_other_shape_value = []
        #     self.mode = "getothershapes-key"
        #
        # if self.mode == "getothershapes-value" and data not in self.ignorable_broad + ["(", ")"]:
        #     self.current_other_shape_value.append(data)
        #
        # if self.mode == "getothershapes-key":  # Not an elif.
        #     self.current_other_shape_key = data
        #
        # if self.mode == "getgender":
        #     self.output_obj["gender"] = add_string(self.output_obj["gender"], data)
        #
        # if self.mode.startswith("getword") and self.lasttag == "a":
        #     word_index = int(self.mode.split("-")[1])
        #     key = self.keys[word_index]
        #     subkey = self.subkey
        #     if subkey not in self.inflections[key]:
        #         self.inflections[key][subkey] = data
        #     else:
        #         if not isinstance(self.inflections[key][subkey], list):
        #             self.inflections[key][subkey] = [self.inflections[key][subkey]]
        #         self.inflections[key][subkey].append(data)
        #
        # if self.mode == "gettingkeys":
        #     key_longhand = data
        #     self.keys.append(case_ref[key_longhand] if key_longhand in case_ref else key_longhand)
        #
        # if self.mode == "gettingsubkey":
        #     subkey_longhand = data
        #     self.subkey = case_ref[subkey_longhand] if subkey_longhand in case_ref else subkey_longhand
        #     self.mode = "getword-0"

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

        if self.mode in ["getpluvirnom", "gettinglemma", "gettingpluvirnom"]:
            if startTag == "tr":
                self.tr_count += 1

            if self.tr_count == 3:
                if startTag == "td":
                    self.td_count += 1
                if self.td_count == 1:
                    self.mode = "gettinglemma"
                elif self.td_count in [2, 3]:
                    self.mode = "getpluvirnom"
                elif self.td_count == 4:
                    self.mode = "gettingpluvirnom"

        if self.mode == "gettranslations" and startTag == "ol":
            self.mode = "gettingtranslations"

        # if self.mode == "gettingusage" and startTag in ["h1", "h2", "h3", "h4"]:
        #     self.output_obj["usage"].append(self.current_usage)
        #     self.mode = None
        #
        # if self.mode in ["getderivedterms", "gettingsynonyms"] and startTag in ["h1", "h2", "h3", "h4"]:
        #     self.mode = None
        #
        # if self.mode == "gettingdefinition" and startTag == "dd":
        #     self.mode = "gettingusage"
        #
        # if self.mode == "getdefinitions" and startTag == "li":
        #     self.mode = "gettingdefinition"
        #
        # if self.mode and self.mode.startswith("getothershapes") and startTag == "ol":
        #     self.mode = "getdefinitions"
        #
        # if self.mode == "getothershapes-key" and startTag == "b":
        #     self.mode = "getothershapes-value"
        #
        # if self.mode == "getothershapes" and startTag == "i":
        #     self.mode = "getothershapes-key"
        #
        # if self.location == "insidetable":
        #     if startTag == "th" and self.mode == "getsubkey":
        #         self.mode = "gettingsubkey"
        #
        #     if startTag == "th" and self.mode == "getkeys":
        #         self.mode = "gettingkeys"
        #
        #     if startTag == "tr" and not self.keys:
        #         self.mode = "getkeys"
        #
        #     if startTag == "table":
        #         self.el_count += 1
        #
        # elif self.location == "insideselectedlang":
        #     if startTag == "span" and self.penultimatetag == "strong":
        #         for attr in attrs:
        #             if attr[0] == "class" and attr[1] == "gender":
        #                 self.mode = "getgender"
        #
        #     elif startTag == "table":
        #         for attr in attrs:
        #             if attr[0] == "class" and attr[1] == "wikitable inflection-table":
        #                 self.location = "insidetable"

    def handle_endtag(self, endTag):
        if self.mode == "gettingpluvirnom" and endTag == "td":
            self.mode = "END"

        if self.mode == "gettingtranslations" and endTag == "ol":
            self.mode = "getpluvirnom"

        if self.mode == "gettingadverb" and endTag == "p":
            self.mode = "gettranslations"

        if self.location == "insideselectedlang" and (endTag == "body" or self.mode == "END"):

            if len(self.output_obj["translations"]) > 1:
                self.output_obj["translations_additional"] = self.output_obj["translations"][1:]
                self.output_obj["translations"] = self.output_obj["translations"][0:1]

            if len(self.output_obj["lemma"]) > 1:
                self.output_arr = []
                return


            self.output_arr.append(self.output_obj)



            self.location = None
            self.mode = None
            # for output_obj in self.output_arr:
            #     if output_obj["usage"]:
            #         usages_copy = output_obj["usage"][:]
            #         for item in usages_copy:
            #             cease = False
            #             for string in [
            #                 "Synonyms: see Thesaurus:",
            #                 "Synonym: see Thesaurus:",
            #                 "Synonyms:",
            #                 "Synonym:",
            #             ]:
            #                 if not cease and item.startswith(string):
            #                     match = re.match(fr"(?P<drop_this>{string}) (?P<keep_this>.+)", item)
            #                     output_obj["synonyms"].append(match["keep_this"])
            #                     output_obj["usage"].remove(item)
            #                     cease = True
            #
            #     for key in ["usage", "otherShapes", "derivedTerms", "synonyms"]:
            #         if not output_obj[key]:
            #             output_obj.pop(key)

        self.lsEndTags.append(endTag)
        self.lsAll.append(endTag)

        # if self.mode == "gettingusage" and endTag == "dd":
        #     self.mode = "gettingdefinition"
        #     self.output_obj["usage"].append(self.current_usage)
        #     self.current_usage = None
        #
        # if self.mode == "gettingdefinition" and endTag == "li":
        #     definition = brackets_to_end(trim_around_brackets(self.current_definition))
        #     self.output_obj["translations"]["ENG"].extend(split_definition_to_list(definition))
        #     self.current_definition = None
        #     self.mode = "getdefinitions"
        #
        # if endTag == "ol" and self.mode == "getdefinitions":
        #     self.mode = None
        #
        # if self.mode and self.mode.startswith("getothershapes") and endTag == "p":
        #     if self.current_other_shape_key != "null" and self.current_other_shape_value:
        #         self.output_obj["otherShapes"][self.current_other_shape_key] = self.current_other_shape_value
        #     self.current_other_shape_key = None
        #     self.current_other_shape_value = []
        #
        # if endTag == "span" and self.mode == "getgender":
        #     self.mode = "getothershapes"
        #
        # if endTag == "span" and self.mode and self.mode.split("-")[0] == "getword":
        #     word_index = int(self.mode.split("-")[1])
        #     self.mode = f"getword-{str(word_index + 1)}"
        #
        # if endTag == "tr":
        #     if self.mode and self.mode.split("-")[0] == "getword":
        #         self.mode = "getsubkey"
        #
        #     elif self.mode == "gettingkeys":
        #         for key_longhand in self.keys:
        #             key = case_ref[key_longhand] if key_longhand in case_ref else key_longhand
        #             self.inflections[key] = {}
        #         self.mode = "getsubkey"
        #
        # if endTag == "table" and self.location == "insidetable":
        #     if self.el_count:
        #         self.el_count -= 1
        #     else:
        #         self.location = "insideselectedlang"
        #         self.output_obj["inflections"] = self.inflections
        #
        #         self.output_obj["gender"] = gender_translation_ref[self.output_obj["gender"]]
        #
        #         if self.output_obj["gender"] in gender_to_tags_ref:
        #             self.output_obj["tags"].extend(gender_to_tags_ref[self.output_obj["gender"]])
        #
        #         if "singular" in self.output_obj["inflections"] and "plural" not in self.output_obj["inflections"]:
        #             self.output_obj["lacking"] = True
        #             self.output_obj["tantumSingulare"] = True
        #         elif "singular" not in self.output_obj["inflections"] and "plural" in self.output_obj["inflections"]:
        #             self.output_obj["lacking"] = True
        #             self.output_obj["tantumPlurale"] = True
        #
        #         self.output_arr.append(self.output_obj)
        #         self.reset_for_new_table()

    def handle_startendtag(self, startendTag, attrs):
        self.lsStartEndTags.append(startendTag)
        self.lsAll.append(startendTag)

    def handle_comment(self, data):
        self.lsComments.append(data)
        self.lsAll.append(data)
