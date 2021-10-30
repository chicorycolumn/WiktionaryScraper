from html.parser import HTMLParser

from utils.scraping.common import orth

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
    ignorable_translations = ["relational"]

    tr_count = 0
    td_count = 0

    def reset_for_new_table(self):
        self.mode = None
        # self.el_count = 0
        # self.inflections = {}
        self.output_obj = {
            "lemma": [],
            "translations": [],
            "comparative_type": None,
            "pluvirnom_lemma": [],
            "adverb": [],
            "comparative": []
        }
        # self.keys = []
        # self.subkey = None
        # self.current_definition = None
        # self.current_usage = None
        # self.current_other_shape_key = None
        # self.current_other_shape_value = []
        self.tr_count = 0
        self.td_count = 0

    def reset_for_new_word(self):
        self.reset_for_new_table()
        self.output_arr = []
        # self.keys = []
        self.location = None

    def handle_data(self, data):
        data = orth(data)

        if not data or data in self.ignorable_narrow + ["(", ")"]:
            return

        if self.location == "insideselectedlang":
            if self.mode == "gettingpluvirnom":
                self.output_obj["pluvirnom_lemma"].append(data)

            if self.mode == "gettinglemma":
                self.output_obj["lemma"].append(data)

            if self.mode == "gettingtranslations":
                data_arr = data.split(",")
                self.output_obj["translations"].extend([w for w in data_arr if w not in self.ignorable_translations])

            if self.mode == "gettingadverb":
                self.output_obj["adverb"].append(data)

            if self.lasttag == "i" and data.lower() == "adverb":
                self.mode = "gettingadverb"

            if self.lasttag == "i" and data.lower() == "superlative":
                self.mode = None

            if self.mode == "gettingcomparative":
                if data not in self.ignorable_broad:
                    self.output_obj["comparative"].append(data)

            if self.mode == "getcomparativeinfo":
                if self.lasttag == "i" and data.lower() == "comparative":
                    self.mode = "gettingcomparative"
                elif self.lasttag == "i" and data.lower() == "not comparable":
                    self.output_obj["comparative_type"] = 0
                    self.mode = "gettranslations"

        if self.penultimatetag in ["h1", "h2", "h3", "h4", "h5"]:
            if self.location == "insideselectedlang":
                if self.lasttag == "span" and data.lower() == "adjective":
                    self.mode = "getcomparativeinfo"
            elif data.lower() == self.selected_lang:
                self.location = "insideselectedlang"

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

        if self.mode in ["handlingtable", "gettinglemma", "gettingpluvirnom"]:
            if startTag == "tr":
                self.tr_count += 1

            if self.tr_count == 3:
                if startTag == "td":
                    self.td_count += 1
                if self.td_count == 1:
                    self.mode = "gettinglemma"
                elif self.td_count in [2, 3]:
                    self.mode = "handlingtable"
                elif self.td_count == 4:
                    self.mode = "gettingpluvirnom"

        if self.location == "insideselectedlang" and self.mode == "readyfortable":
            if startTag == "table" and "inflection-table" in self.currentclass.split(" "):
                self.mode = "handlingtable"

        if self.mode == "gettranslations" and startTag == "ol":
            self.mode = "gettingtranslations"

    def handle_endtag(self, endTag):
        if self.mode == "gettingpluvirnom" and endTag == "td":
            self.mode = "END"

        if self.mode == "gettingtranslations" and endTag == "ol":
            self.mode = "readyfortable"

        if self.mode == "gettingadverb" and endTag == "p":
            self.mode = "gettranslations"

        if self.mode == "getcomparativeinfo":
            if endTag == "p" and not self.output_obj["comparative_type"]:
                self.output_obj["comparative_type"] = 0
                self.mode = "gettranslations"

        if self.mode and self.location == "insideselectedlang" and (endTag == "body" or self.mode == "END"):

            if len(self.output_obj["lemma"]) != 1:
                print(f'#ERR Wrong number of lemmas {self.output_obj["lemma"]}')
                return

            lemma = self.output_obj["lemma"]
            self.output_obj.pop("lemma")
            self.output_obj["lemma"] = lemma

            self.output_obj["tags"] = "xxxxxxxxx"

            translations = self.output_obj["translations"]
            self.output_obj.pop("translations")
            self.output_obj["translations"] = translations

            if len(self.output_obj["translations"]) > 1:
                self.output_obj["translations_additional"] = self.output_obj["translations"][1:]
                self.output_obj["translations"] = self.output_obj["translations"][0:1]

            if len(self.output_obj["comparative"]) == 0:
                if self.output_obj["comparative_type"] == 0:
                    self.output_obj.pop("comparative")
                    if len(self.output_obj["adverb"]):
                        print(f'#ERR Not comparable and yet is adverb? {self.output_obj["adverb"]}')
                        return
                    else:
                        self.output_obj.pop("adverb")
                else:
                    print(f'#ERR Did not collect enough comparatives {self.output_obj["comparative"]}')
                    return

            elif len(self.output_obj["comparative"]) == 1:
                self.output_obj["comparative_type"] = 1
                self.output_obj["comparative"] = self.output_obj["comparative"][0]
            elif len(self.output_obj["comparative"]) == 2 and self.output_obj["comparative"][0] == "bardziej":
                self.output_obj["comparative_type"] = 2
                self.output_obj.pop("comparative")
            elif len(self.output_obj["comparative"]) == 3:
                if self.output_obj["comparative"][0] == "bardziej":
                    self.output_obj["comparative_type"] = 3
                    self.output_obj["comparative"] = self.output_obj["comparative"][2]
                elif self.output_obj["comparative"][1] == "bardziej":
                    self.output_obj["comparative_type"] = 3
                    self.output_obj["comparative"] = self.output_obj["comparative"][0]
                else:
                    print(f'#ERR Wrong order of comparatives {self.output_obj["comparative"]}')
                    return
            else:
                print(f'#ERR Wrong number of comparatives {self.output_obj["comparative"]}')
                print(f'#ERR Wrong number of comparatives {self.output_obj["comparative"]}')
                return

            self.output_arr.append(self.output_obj)
            self.location = None
            self.mode = None
            return

        self.lsEndTags.append(endTag)
        self.lsAll.append(endTag)

    def handle_startendtag(self, startendTag, attrs):
        self.lsStartEndTags.append(startendTag)
        self.lsAll.append(startendTag)

    def handle_comment(self, data):
        self.lsComments.append(data)
        self.lsAll.append(data)
