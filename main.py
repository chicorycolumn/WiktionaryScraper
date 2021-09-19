import html.entities
import json
from html.parser import HTMLParser
from html import entities
import urllib.request as urllib2
import urllib as urllib
from datetime import datetime
from time import sleep


def parse(head_words: dict = None, use_sample: bool = False):
    parse_inflection_tables = MyHTMLParser(convert_charrefs=False)

    if not head_words:
        head_words = ["małpa"]

    result = {}

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

        if output_arr:
            print("Adding output_arr to result:", output_arr)
            result[head_word] = output_arr
        else:
            print(f"# No output created for {head_word}")

        sleep(2)

    print("Writing result.")
    write_output(result)

    # print("Data", parser.lsData)
    # print("Start tags", parser.lsStartTags)
    # print("End tags", parser.lsEndTags)
    # print("Start End tags", parser.lsStartEndTags)
    # print("Comments", parser.lsComments)


class MyHTMLParser(HTMLParser):
    # Initializing lists
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
    el_count = 0
    output = {}
    output_arr = []
    keys = []
    subkey = None
    selected_lang = "polish"

    def reset_for_new_table(self):
        self.mode = None
        self.el_count = 0
        self.output = {}
        self.keys = []
        self.subkey = None

    def handle_data(self, data):

        if superstrip(data) and superstrip(data) not in ["/", ","]:
            if self.location not in ["insideselectedlang", "insidetable"]:
                if self.lasttag == "span" and self.penultimatetag == "h2":
                    lang_in_focus = superstrip(data).lower()
                    if lang_in_focus == self.selected_lang:
                        print(f"#------------------------>ENTERING SELECTED LANG", 'self.location = "insideselectedlang"')
                        self.location = "insideselectedlang"
                    else:
                        self.location = None

            if self.mode and self.mode.split("-")[0] == "getword" and self.lasttag == "a":
                word_index = int(self.mode.split("-")[1])
                key = self.keys[word_index]
                subkey = self.subkey
                if subkey not in self.output[key]:
                    self.output[key][subkey] = orth(data)
                else:
                    self.output[key][subkey] = [self.output[key][subkey]]
                    self.output[key][subkey].append(orth(data))

            if self.mode == "gettingkeys":
                print(f"#------------------------>GETTING {orth(data)}")
                self.keys.append(orth(data))

            if self.mode == "gettingsubkey":
                print(f"#------------------------>GETTING {orth(data)}")
                self.subkey = orth(data)
                self.mode = "getword-0"

        # if self.mode == "getdata":
        #     key = self.keys[-1]
        #
        #     if key not in self.output:
        #         self.output[key] = []
        #
        #     self.output[key].append(data)
        #     self.mode = None
        #
        # print("DATA:", data)
        # self.lsData.append(data)
        # self.lsAll.append(data)

    def handle_starttag(self, startTag, attrs):
        self.penultimatetag = self.lasttag_copy
        self.lasttag_copy = startTag
        print("S TAG:", startTag)
        self.lsStartTags.append(startTag)
        self.lsAll.append(startTag)

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

        elif startTag == "table" and self.location == "insideselectedlang":
            for attr in attrs:
                print("attr", attr)
                if attr[0] == "class" and attr[1] == "wikitable inflection-table":
                    print("#------------------------>ENTERING INFLECTION TABLE", 'self.location = "insidetable""')
                    self.location = "insidetable"

        # if startTag == "p" and self.location == "insidediv" and not self.el_count:
        #     self.mode = "getdata"

        # for attr in attrs:
        #     self.lsAll.append(attr)
        #     if attr[0] == "title":
        #         self.keys.append(attr[1])
        #
        #     if attr[0] == "class" and attr[1] == "group":
        #         # self.mode = "getkey"
        #         self.location = "insidediv"
        #         self.el_count = 0

    def handle_endtag(self, endTag):
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
                    self.output[key] = {}
                self.mode = "getsubkey"

        if endTag == "table" and self.location == "insidetable":
            if self.el_count:
                self.el_count -= 1
            else:
                self.location = "insideselectedlang"
                self.output_arr.append(self.output)
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
            # "plural": {
            #     "nom": "małpy",
            #     "gen": "małp"
            # },
        }

    # json_object = json.dumps(dict, indent=4)
    json_object = json.dumps(dict, indent=4, ensure_ascii=False)

    with open("output/output.json", "w") as outfile:
        outfile.write(json_object)


def html_from_head_word(head_word):
    print(datetime.now().strftime('%H:%M:%S'), f"{head_word} is being loaded up as a Wiktionary page.")
    html_page = urllib2.urlopen(f"https://en.wiktionary.org/wiki/{urllib.parse.quote(head_word)}")
    return str(html_page.read())


def orth(str):
    return double_decode(superstrip(str))


def superstrip(str):
    return str.replace("\\n", "").strip()


def double_decode(str):
    return str.encode('utf-8').decode('unicode-escape').encode('iso-8859-1').decode('utf-8')
    # source: https://stackoverflow.com/a/49756591
    # 1. actually any encoding support printable ASCII would work, for example utf-8
    # 2. unescape the string, see https://stackoverflow.com/a/1885197
    # 3. latin-1 also works, see https://stackoverflow.com/q/7048745
    # 4. finally decode again


if __name__ == '__main__':
    # Sample ser has meanings in many languages, but we only want the Polish one.
    # Sample rok has that too, but also, it has two inflection tables in Polish, and we want both.
    parse(["rok"], True)
    # write_output()
