import copy
from html.parser import HTMLParser

from utils.general.common import write_todo
from utils.scraping.Polish_dicts import aspect_ref
from utils.scraping.common import orth, superstrip, add_string, trim_chaff_from_derived_terms, add_value_at_keychain


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

    current_otherShapes_key = None
    current_otherShapes_value = []

    row_num = 0
    col_num = 0
    ingested_table = []
    current_cell_rowspan = 1
    current_cell_colspan = 1
    current_row_data = []
    current_derived_term = []
    diff_word_same_conj_count = 0
    diff_word_same_conj_objects = []

    got_derived_terms = False
    got_related_terms = False

    def add_lobj_and_reset(self, diff_word_same_conj: bool = False):
        print("add_lobj_and_reset", "\n")

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
        print("#####", self.output_obj["aspect"])
        if len(self.output_obj["aspect"]) != 1:
            print(
                f'#ERR self.output_obj["aspect"] is {type(self.output_obj["aspect"])} {self.output_obj["aspect"]} should have length 1')
            return
        else:
            self.output_obj["aspect"] = aspect_ref[self.output_obj["aspect"][0]]

        if diff_word_same_conj:
            self.output_obj["diff_word_same_conj"] = True
        else:
            for out_obj in self.output_arr:
                if "diff_word_same_conj" in out_obj and out_obj["diff_word_same_conj"]:
                    out_obj["derivedTerms"] = copy.deepcopy(self.output_obj["derivedTerms"])
                    out_obj["inflections"] = copy.deepcopy(self.output_obj["inflections"])
                    out_obj["allohomInfo"] = None
                    write_todo(f'At least two lobjs of "{out_obj["lemma"]}" needs allohomInfo added.')
                    self.output_obj["allohomInfo"] = None
                    out_obj.pop("diff_word_same_conj")

        self.output_arr.append(self.output_obj)
        self.reset_for_new_table()

    def generate_empty_output_object(self):
        return {
            "lemma": None,
            "aspect": [],
            "secondaryAspects": [],
            "otherShapes": {},
            "tags": "xxxxxxxxx",
            "translations": {"ENG": []},
            "derivedTerms": []
        }

    def add_new_row_obj(self):
        self.ingested_table.append({
                "closed": False,
                "data": []
            })

    def reset_for_new_cell(self):
        print("reset_for_new_cell")
        self.current_cell_rowspan = 1
        self.current_cell_colspan = 1
        self.current_row_data = []

    def reset_for_new_table(self):
        print("reset_for_new_table", "\n")
        self.reset_for_new_cell()

        self.mode = None
        print('mode = None (reset_for_new_table)')
        self.el_count = 0
        self.inflections = {}
        self.output_obj = self.generate_empty_output_object()
        self.keys = []
        self.subkey = None
        self.current_definition = None
        self.current_usage = None

        self.current_otherShapes_key = None
        self.current_otherShapes_value = []
        self.row_num = 0
        self.col_num = 0
        self.ingested_table = []
        self.current_derived_term = []
        self.diff_word_same_conj_count = 0
        self.diff_word_same_conj_objects = []

    def reset_for_new_word(self):
        print("reset_for_new_word", "\n")
        self.got_derived_terms = False
        self.got_related_terms = False
        self.reset_for_new_table()
        self.output_arr = []
        self.keys = []
        self.location = None
        print('location = None')

    def handle_data(self, data):
        data = orth(data)

        if not data or data in self.ignorable_narrow:
            if self.location == "insidetable":
                if data not in [","]:
                    return
            else:
                return

        if self.location in ["insideselectedlang", "insideword"] \
                and \
                (
                        (self.penultimatetag in ["h1", "h2", "h3", "h4", "h5"] and self.lasttag == "span" and data.lower() == "verb")
                 or
                        (self.mode == "gettable" and self.lastclass == "Latn headword")
                ):

            self.location = "insideword"
            print('location = "insideword"')
            self.diff_word_same_conj_count += 1

            if self.diff_word_same_conj_count > 1:
                self.add_lobj_and_reset(diff_word_same_conj = True)

            self.mode = "getaspect"
            print('mode = "getaspect"')

        if self.location == "insideword":
            if self.lasttag in ["h1", "h2", "h3", "h4", "h5"] or self.penultimatetag in ["h1", "h2", "h3", "h4", "h5"]:
                split = data.split(" ")
                if split[0].lower() == "etymology" and len(split) > 1 and int(split[1]) > 1:
                    self.location = "insideselectedlang"
                    print('location = "insideselectedlang"')
                    self.add_lobj_and_reset()

            if self.mode == "gettingderivedterms":
                self.current_derived_term.append(data)

            if self.mode == "getderivedterms":
                if self.lasttag in ["h1", "h2", "h3", "h4", "h5"] or self.penultimatetag in ["h1", "h2", "h3", "h4", "h5"]:
                    if data.lower() in ["derived terms", "related terms"]:
                        self.mode = "gettingderivedterms"
                        print('mode = "gettingderivedterms"')
                    else:
                        self.mode = "getderivedterms"
                        print('mode = "getderivedterms"')

            if self.mode == "gettingdefinition":
                self.current_definition = add_string(self.current_definition, data)

            if self.mode == "getaspect":
                if data in ["(", ")"]:
                    return

                if self.lasttag == "i":
                    self.current_otherShapes_key = data

                if "b" in [self.penultimatetag, self.lasttag]:
                    self.current_otherShapes_value.append(data)

                if self.lasttag == "abbr":
                    self.output_obj["aspect"].append(data)

                if self.lastclass == "Latn headword":
                    self.output_obj["lemma"] = data

        if self.location == "insidetable":
            self.current_row_data.append(data)
        else:
            if self.lasttag == "span" and self.penultimatetag == "h2":
                lang_in_focus = superstrip(data).lower()
                if lang_in_focus == self.selected_lang:
                    self.location = "insideselectedlang"
                    print('location = "insideselectedlang"')
                else:
                    if self.location in ["insideselectedlang", "insideword"]:
                        self.mode = "END"
                        print('mode = "END"')
                    self.location = None
                    print('location = None')


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

        if self.location == "insideword":
            if self.mode == "gettable":
                if startTag == "table" and self.currentclass and "inflection-table" in self.currentclass.split(" "):
                    self.mode = None
                    print('mode = None (startTag == "table" and self.currentclass and "inflection-table"...)')
                    self.location = "insidetable"
                    print('location = "insidetable"')

            if self.mode == "getdefinitions" and startTag == "li":
                self.mode = "gettingdefinition"
                print('mode = "gettingdefinition"')

            if self.mode == "getaspect":
                if startTag in ["i", "ol"]:
                    if self.current_otherShapes_value:
                        self.output_obj["otherShapes"][self.current_otherShapes_key] = self.current_otherShapes_value[:]
                        self.current_otherShapes_key = None
                        self.current_otherShapes_value = []
                    elif self.current_otherShapes_key:
                        self.output_obj["secondaryAspects"].append(self.current_otherShapes_key)
                if startTag == "ol":
                    self.mode = "getdefinitions"
                    print('mode = "getdefinitions"')

    def handle_endtag(self, endTag):
        if self.mode and (self.mode == "END" or endTag in ["body", "html"]):
            print("ENDING")
            self.add_lobj_and_reset()
            self.location = None
            print('location = None')
            self.mode = None
            print('mode = None (ENDING)')
            aalobj = self.output_obj
            aaouta = self.output_arr
            return

        if self.location == "insidetable":
            if endTag == "table":
                self.location = "insideword"
                print('location = "insideword"')
                self.mode = "getderivedterms"
                print('mode = "getderivedterms"')

            elif endTag == "tr":
                self.mode = None
                print('mode = None (self.location == "insidetable" and endTag == "tr")')
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

                self.reset_for_new_cell()

        if self.mode == "gettingderivedterms" and endTag == "li":
            derived_term = trim_chaff_from_derived_terms(" ".join(self.current_derived_term), self.output_obj['lemma'])
            if "further reading" not in derived_term.lower() and f"in {self.selected_lang} dictionaries" not in derived_term.lower():
                self.current_derived_term = []
                if derived_term:
                    self.output_obj["derivedTerms"].append(derived_term)

        if self.mode == "gettingdefinition" and endTag == "li":
            # definition = brackets_to_end(trim_around_brackets(self.current_definition))
            self.output_obj["translations"]["ENG"].append(self.current_definition)
            self.current_definition = None
            self.mode = "getdefinitions"
            print('mode = "getdefinitions"')

        if endTag == "ol" and self.mode == "getdefinitions":
            self.mode = "gettable"
            print('mode = "gettable"')

        self.lsEndTags.append(endTag)
        self.lsAll.append(endTag)

    def handle_startendtag(self, startendTag, attrs):
        self.lsStartEndTags.append(startendTag)
        self.lsAll.append(startendTag)

    def handle_comment(self, data):
        self.lsComments.append(data)
        self.lsAll.append(data)
