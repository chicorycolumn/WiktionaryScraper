import html.entities
import json
from html.parser import HTMLParser
from html import entities
import urllib.request as urllib2
import urllib as urllib
from datetime import datetime
from time import sleep
import re


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
    print("\n", datetime.now().strftime('%H:%M:%S'), f"{head_word} is being loaded up as a Wiktionary page.", "\n")
    html_page = urllib2.urlopen(f"https://en.wiktionary.org/wiki/{urllib.parse.quote(head_word)}")
    return str(html_page.read())


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
    return str.encode('utf-8').decode('unicode-escape').encode('iso-8859-1').decode('utf-8')
    # source: https://stackoverflow.com/a/49756591
    # 1. actually any encoding support printable ASCII would work, for example utf-8
    # 2. unescape the string, see https://stackoverflow.com/a/1885197
    # 3. latin-1 also works, see https://stackoverflow.com/q/7048745
    # 4. finally decode again


def scrape_word_data(language: str, parser, head_words: dict = None, use_sample: bool = False):
    if not head_words:
        head_words = ["małpa"]

    result = []

    for head_word in head_words:
        output_arr = None

        if use_sample:
            with open(f'input/{language}/sample_{head_word}.html', 'r') as f:
                contents = f.read()
                parser.feed(contents)
                output_arr = parser.output_arr
                f.close()
        else:
            try:
                html_string = html_from_head_word(head_word)
                parser.feed(html_string)
                output_arr = parser.output_arr
                parser.output_arr = []
            except:
                print("\n", f'# Failed to read html for "{head_word}"', "\n")

        if output_arr:
            print("Adding output_arr to result:", output_arr)
            for lemma_object in output_arr:
                lemma_object["lemma"] = head_word
            result.extend(output_arr)
        else:
            print("\n", f'# Successfully read html but created no output for "{head_word}"', "\n")

        print("Writing result.")
        write_output(result)

        if not use_sample:
            sleep(1)