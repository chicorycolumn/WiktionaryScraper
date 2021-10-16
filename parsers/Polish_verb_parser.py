from scraper_utils.common import *
from scraper_utils.Polish import *
from html.parser import HTMLParser
from copy import deepcopy
import re


class PolishVerbParser(HTMLParser):
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

    current_other_shapes_key = None
    current_other_shapes_value = []

    row_num = 0
    col_num = 0
    ingested_table = []
    current_cell_rowspan = 1
    current_cell_colspan = 1
    current_row_data = []

    def add_new_row_obj(self):
        self.ingested_table.append({
                "closed": False,
                "data": []
            })

    def reset_for_new_cell(self):
        self.current_cell_rowspan = 1
        self.current_cell_colspan = 1
        self.current_row_data = []

    def reset_for_new_table(self):
        self.reset_for_new_cell()

        self.mode = None
        self.el_count = 0
        self.inflections = {}
        self.output_obj = {
            "lemma": None,
            "aspect": [],
            "secondary_aspects": [],
            "other_shapes": {},
            "tags": "xxxxxxxxx",
            "translations_info": [],
            "translations": {"ENG": []},
            # "id": None,
            # "usage": [],
            # "otherShapes": {},
            # "derivedTerms": [],
            # "synonyms": [],
            # "inflections": {},
        }
        self.keys = []
        self.subkey = None
        self.current_definition = None
        self.current_usage = None
        self.current_other_shape_key = None
        self.current_other_shape_value = []

        self.current_other_shapes_key = None
        self.current_other_shapes_value = []
        self.row_num = 0
        self.col_num = 0
        self.ingested_table = []


    def reset_for_new_word(self):
        self.reset_for_new_table()
        self.output_arr = []
        self.keys = []
        self.location = None

    def handle_data(self, data):
        data = orth(data)

        if not data or data in self.ignorable_narrow:
            if self.location == "insidetable":
                if data not in [","]:
                    return
            else:
                return

        if self.location == "insidetable":
            self.current_row_data.append(data)

        if self.location == "insideselectedlang":
            if self.mode == "gettingdefinition":
                self.current_definition = add_string(self.current_definition, data)

            if self.mode == "getaspect":
                if data in ["(", ")"]:
                    return

                if self.lasttag == "i":
                    self.current_other_shapes_key = data

                if "b" in [self.penultimatetag, self.lasttag]:
                    self.current_other_shapes_value.append(data)

                if self.lasttag == "abbr":
                    self.output_obj["aspect"].append(data)

                if self.lastclass == "Latn headword":
                    self.output_obj["lemma"] = data

        if self.penultimatetag in ["h1", "h2", "h3", "h4", "h5"]:
            if self.location == "insideselectedlang":
                if self.lasttag == "span" and data.lower() == "verb":
                    self.mode = "getaspect"

            elif data.lower() == self.selected_lang:
                self.location = "insideselectedlang"

        # if self.location == "insideselectedlang" and self.penultimatetag in ["h1", "h2", "h3", "h4", "h5"]:
        #     # Mode setting from within handle_data, which is not typical.
        #
        #     if self.lasttag == "span" and data.lower() == "usage notes":
        #         self.mode = "gettingusage"
        #
        #     if self.lasttag == "span" and data.lower() == "synonyms":
        #         self.mode = "gettingsynonyms"
        #
        #     if data.lower() == "derived terms":
        #         self.mode = "getderivedterms"
        #
        # if self.location != "insidetable":
        #     if self.lasttag == "span" and self.penultimatetag == "h2":
        #         lang_in_focus = superstrip(data).lower()
        #         if lang_in_focus == self.selected_lang:
        #             self.location = "insideselectedlang"
        #         else:
        #             self.location = None
        #
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
            elif attr[0] == "rowspan":
                self.current_cell_rowspan = int(attr[1])
            elif attr[0] == "colspan":
                self.current_cell_colspan = int(attr[1])

        if self.location == "insidetable":
            if startTag == "tr":
                while len(self.ingested_table) <= self.row_num:
                    self.add_new_row_obj()

        if self.location == "insideselectedlang":
            if self.mode == "gettable":
                if startTag == "table" and "inflection-table" in self.currentclass.split(" "):
                    self.mode = None
                    self.location = "insidetable"

            if self.mode == "getdefinitions" and startTag == "li":
                self.mode = "gettingdefinition"

            if self.mode == "getaspect":
                if startTag in ["i", "ol"]:
                    if self.current_other_shapes_value:
                        self.output_obj["other_shapes"][self.current_other_shapes_key] = self.current_other_shapes_value[:]
                        self.current_other_shapes_key = None
                        self.current_other_shapes_value = []
                    elif self.current_other_shapes_key:
                        self.output_obj["secondary_aspects"].append(self.current_other_shapes_key)
                if startTag == "ol":
                    self.mode = "getdefinitions"

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
        if self.location == "insidetable":
            if endTag == "table":

                def add_value_at_keychain(value, keychain, dict):
                    for index, key in enumerate(keychain):
                        if key not in dict:
                            dict[key] = {}
                        if index + 1 == len(keychain):
                            dict[key] = value
                        else:
                            dict = dict[key]

                t = [row["data"] for row in self.ingested_table]
                inflections = {}
                index_of_first_data_row = 0
                header_rows = []

                for index, row in enumerate(t):
                    if all(type(item) is str and item.startswith("#") for item in row):
                        header_rows.append(row)
                    else:
                        index_of_first_data_row = index
                        break

                for list_index, list in enumerate(t[index_of_first_data_row:]):
                    keychain_base = []

                    for cell in list:
                        if type(cell) == str and cell.startswith("#"):
                            if not len(keychain_base) or cell not in keychain_base:
                                keychain_base.append(cell)

                    for cell_index, cell in enumerate(list):
                        if type(cell) is not str or not cell.startswith("#"):
                            keychain = keychain_base[:]
                            for header_row in header_rows:
                                if not header_row[cell_index].startswith("#"):
                                    print("# Error 151")
                                keychain.append(header_row[cell_index])

                            if cell != "<blank>":
                                add_value_at_keychain(cell, [k[1:] for k in keychain], inflections)

                self.output_obj["inflections"] = inflections

                if len(self.output_obj["aspect"]) != 1:
                    print(f'#ERR len(self.output_obj["aspect"]) is {len(self.output_obj["aspect"])} should be 1')
                    return
                else:
                    self.output_obj["aspect"] = aspect_ref[self.output_obj["aspect"][0]]

                for tinfo in self.output_obj["translations_info"][:]:
                    search1 = re.search(r"(?P<first_bracketed>\(.*?\))", tinfo)
                    if re.search(r"reflexive", search1["first_bracketed"]): #Requires "się".
                        copied_lemma_object = deepcopy(self.output_obj)
                        copied_lemma_object["translations_info"] = [tinfo]
                        copied_lemma_object["reflexive"] = True
                        self.output_arr.append(copied_lemma_object)
                        self.output_obj["translations_info"] = [t for t in self.output_obj["translations_info"] if t != tinfo]
                    if re.search(r"impersonal", search1["first_bracketed"]): #Requires "się".
                        copied_lemma_object = deepcopy(self.output_obj)
                        copied_lemma_object["translations_info"] = [tinfo]
                        copied_lemma_object["impersonal"] = True
                        self.output_arr.append(copied_lemma_object)
                        self.output_obj["translations_info"] = [t for t in self.output_obj["translations_info"] if t != tinfo]


                self.output_arr.insert(0, self.output_obj)
                self.location = None
                self.mode = None
                aalobj = self.output_obj
                aaouta = self.output_arr
                return

            elif endTag == "tr":
                self.mode = None
                self.ingested_table[self.row_num]["closed"] = True
                self.row_num += 1

            elif endTag in ["th", "td"]:
                row_data = f'{"#" if endTag == "th" else ""}{" ".join(self.current_row_data if self.current_row_data else ["<blank>"])}'
                if " , " in row_data:
                    row_data = row_data.split(" , ")

                self.current_row_data = []
                self.col_num = len(self.ingested_table[self.row_num]["data"])

                for row_i in range(self.current_cell_rowspan):
                    for col_i in range(self.current_cell_colspan):
                        row_index = self.row_num + row_i
                        col_index = self.col_num + col_i

                        while len(self.ingested_table) <= row_index:
                            t = self.ingested_table
                            self.add_new_row_obj()

                        row_obj = self.ingested_table[row_index]

                        while len(row_obj["data"]) <= col_index:
                            row_obj["data"].append("")

                        row_obj["data"][col_index] = row_data

                        print(f'Added row data "{row_data}" at {row_index}-{col_index}')

                self.reset_for_new_cell()

        if self.mode == "gettingdefinition" and endTag == "li":
            # definition = brackets_to_end(trim_around_brackets(self.current_definition))
            self.output_obj["translations_info"].append(self.current_definition)
            self.current_definition = None
            self.mode = "getdefinitions"

        if endTag == "ol" and self.mode == "getdefinitions":
            self.mode = "gettable"
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

        self.lsEndTags.append(endTag)
        self.lsAll.append(endTag)

    def handle_startendtag(self, startendTag, attrs):
        self.lsStartEndTags.append(startendTag)
        self.lsAll.append(startendTag)

    def handle_comment(self, data):
        self.lsComments.append(data)
        self.lsAll.append(data)
