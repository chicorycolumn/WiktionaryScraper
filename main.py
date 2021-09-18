import html.entities
import json
from html.parser import HTMLParser
from html import entities
import urllib.request as urllib2
import urllib as urllib
from datetime import datetime
from time import sleep


def parse(head_words: dict = None):
    parser = MyHTMLParser()

    if not head_words:
        head_words = ["małpa"]

    for head_word in head_words:
        # print(datetime.now().strftime('%H:%M:%S'), f"{head_word} is being loaded up as a Wiktionary page.")
        # html_page = urllib2.urlopen(f"https://en.wiktionary.org/wiki/{urllib.parse.quote(head_word)}#Polish")
        # parser.feed(str(html_page.read()))

        with open('output/sample_małpa.html', 'r') as f:
            contents = f.read()
            print(type(contents))
            parser.feed(contents)
            print("Output", parser.output)

        parser.feed()
        print("Output", parser.output)
        # print("Data", parser.lsData)
        # print("Start tags", parser.lsStartTags)
        # print("End tags", parser.lsEndTags)
        # print("Start End tags", parser.lsStartEndTags)
        # print("Comments", parser.lsComments)

        # write_output()
        # sleep(2)


class MyHTMLParser(HTMLParser):
    # Initializing lists
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
    keys = []
    subkey = None

    def handle_data(self, data):

        if data.strip():
            if self.mode and self.mode.split("-")[0] == "getword" and self.lasttag == "a":
                word_index = int(self.mode.split("-")[1])
                self.output[self.keys[word_index]][self.subkey] = data.strip()
                self.mode = f"getword-{str(word_index+1)}"

            if self.mode == "gettingkeys":
                print(f"#GETTING {data.strip()}")
                self.keys.append(data.strip())

            if self.mode == "gettingsubkey":
                print(f"#GETTING {data.strip()}")
                self.subkey = data.strip()
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
        print("S TAG:", startTag)
        self.lsStartTags.append(startTag)
        self.lsAll.append(startTag)

        if self.location == "insidetable":
            if startTag == "th" and self.mode == "getsubkey":
                print("#GET SUBKEY")
                self.mode = "gettingsubkey"

            if startTag == "th" and self.mode == "getkeys":
                print("#GET TH")
                self.mode = "gettingkeys"

            if startTag == "tr" and not self.keys:
                print("#ENTERING HEADER TR")
                self.mode = "getkeys"

            if startTag == "table":
                self.el_count += 1

        elif startTag == "table":
            for attr in attrs:
                print("attr", attr)
                if attr[0] == "class" and attr[1] == "wikitable inflection-table":
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
        if endTag == "tr":
            if self.mode and self.mode.split("-")[0] == "getword":
                print("#EXITING GETWORD")
                self.mode = "getsubkey"

            elif self.mode == "gettingkeys":
                print("#EXITING HEADER TR")
                for key in self.keys:
                    self.output[key] = {}
                self.mode = "getsubkey"

        if endTag == "table" and self.location == "insidetable":
            if self.el_count:
                self.el_count -= 1
            else:
                self.location = None

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
                "nom": "małpa",
                "gen": "małpy"
            },
            "plural": {
                "nom": "małpy",
                "gen": "małp"
            },
        }

    json_object = json.dumps(dict, indent=4)

    with open("output/sample_małpa.json", "w") as outfile:
        outfile.write(json_object)


if __name__ == '__main__':
    parse()
