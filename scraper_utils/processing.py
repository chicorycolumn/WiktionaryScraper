import json
import urllib.request as urllib2
import urllib as urllib
from datetime import datetime, timedelta
from time import sleep
import re
from scraper_utils.common import *

shorthand_tag_ref = {
    "h": {
        "tags": ["holdable", "concrete"],
        "topics": [],
    },
    "m": {
        "tags": ["manmade", "concrete"],
        "topics": [],
    },
    "n": {
        "tags": ["natural", "concrete"],
        "topics": [],
    },
    "s": {
        "tags": ["school"],
        "topics": [],
    },
    "w": {
        "tags": ["work"],
        "topics": [],
    },

    # # # # # # # # # # #

    "c": {
        "tags": ["material", "uncountable", "concrete"],
        "topics": ["basic"],
    },
    "¢": {
        "tags": ["chemical", "c"],
        "topics": ["science"],
    },
    "b": {
        "tags": ["bodypart", "concrete"],
        "topics": ["at the doctor", "basic", "body"],
    },
    "ß": {
        "tags": ["schoolsubject", "abstract"],
        "topics": ["school"],
    },
    "w": {
        "tags": ["weather", "abstract", "uncountable"],
        "topics": ["basic", "outdoor"],
    },
    "!": {
        "tags": ["noise", "abstract"],
        "topics": ["sense and perception"],
    },
    "e": {
        "tags": ["emotion", "abstract"],
        "topics": ["inside your head"],
    },
    "$": {
        "tags": ["money"],
        "topics": ["shopping", "maths", "travel"],
    },
    "@": {
        "tags": ["measurement"],
        "topics": ["maths"],
    },
    "at": {
        "tags": ["abstract", "time"],
        "topics": ["travel", "maths"],
    },
    "as": {
        "tags": ["abstract"],
        "topics": ["school"],
    },
    "aw": {
        "tags": ["abstract"],
        "topics": ["work"],
    },
    "ag": {
        "tags": ["abstract"],
        "topics": ["geometric", "maths"],
    },
    "aa": {
        "tags": ["abstract"],
        "topics": [],
    },
    "r": {
        "tags": ["relative", "person", "living", "concrete"],
        "topics": ["relationships"],
    },
    "j": {
        "tags": ["profession", "person", "living", "concrete"],
        "topics": ["work"],
    },
    "a": {
        "tags": ["animal", "living", "concrete"],
        "topics": ["outside"],
    },
    "æ": {
        "tags": ["pet", "animal", "living", "concrete"],
        "topics": ["home", "inside"],
    },
    "t": {
        "tags": ["title", "person", "living", "concrete"],
        "topics": [],
    },
    "p": {
        "tags": ["person", "living", "concrete"],
        "topics": [],
    },
    "f": {
        "tags": ["food", "h"],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "d": {
        "tags": ["drink", "h"],
        "topics": ["kitchen", "restaurant", "inside"],
    },
    "da": {
        "tags": ["alcoholic", "d"],
        "topics": ["kitchen", "restaurant", "nightclub", "inside"],
    },
    "g": {
        "tags": ["clothes", "h"],
        "topics": ["basic"],
    },
    "lg": {
        "tags": ["location", "concrete"],
        "topics": [],
    },
    "lb": {
        "tags": ["location", "building", "concrete"],
        "topics": ["inside"],
    },
    "lr": {
        "tags": ["location", "room", "concrete"],
        "topics": ["inside"],
    },
    "ln": {
        "tags": ["location", "natural", "concrete"],
        "topics": ["outside"],
    },
    "ls": {
        "tags": ["special location", "abstract"],
        "topics": ["religion"],
    },
    "hf": {
        "tags": ["furniture", "concrete"],
        "topics": ["home", "inside"],
    },
    "hh": {
        "tags": ["household objects", "h"],
        "topics": ["home", "inside"],
    },
    "hf": {
        "tags": ["furniture", "concrete"],
        "topics": ["home", "inside"],
    },
    "hb": {
        "tags": ["hh"],
        "topics": ["home", "inside", "bedroom"],
    },
    "hk": {
        "tags": ["hh"],
        "topics": ["home", "inside", "kitchen"],
    },
    "hw": {
        "tags": ["hh"],
        "topics": ["home", "inside", "washroom"],
    },
    "hp": {
        "tags": ["part of house", "concrete"],
        "topics": ["home", "inside"],
    }
}


def recursively_expand_tags(input_stags: list, ref: object):
    output_tags = []

    def rat_inner(input_tags: list):
        for tag in input_tags:
            if tag in ref:
                print(111, tag)
                rat_inner(ref[tag]["tags"])
            elif tag not in output_tags:
                print(222, tag)
                output_tags.append(tag)

    rat_inner(input_stags)
    return output_tags


def add_tags_from_shorthand(lemma_object):
    shorthand_tags = lemma_object["tags"].split(",")
    tags = []
    topics = []

    for stag in shorthand_tags:
        for tag in shorthand_tag_ref[stag]["tags"]:

            if tag in shorthand_tag_ref:
                shorthand_tag_ref
            else:
                if tag not in tags:
                    tags.append(tag)


def untruncate_lemma_objects(group_numbers):
    for group_number in group_numbers:
        res_arr = []

        with open(f"../output_saved/output_nouns_{group_number}.json", "r") as f:
            nouns_long = json.load(f)
        with open(f"../output_saved/truncated_nouns_{group_number}.json", "r") as f:
            nouns_truncated = json.load(f)

        for lemma_object in nouns_truncated:
            lemma_object_long = [lol for lol in nouns_long if lol["temp_id"] == get_base_id(lemma_object["temp_id"])][0]

            for key in lemma_object_long:
                if key not in lemma_object:
                    lemma_object[key] = lemma_object_long[key]

            res_arr.append(lemma_object)

        write_output(res_arr, f"finished_nouns_{group_number}", "../output_saved")


def scrape_word_data(
        parser,
        language: str,
        head_words: dict,
        use_sample: bool,
        filepaths,
        group_number: int = int(str(datetime.now())[-3:]),
        no_temp_ids: bool = False
):
    if not head_words:
        head_words = ["małpa"]

    count = 1

    result = []
    rejected = {"failed_to_load_html": [], "loaded_html_but_failed_when_reading": [],
                "loaded_and_read_html_but_failed_to_create_output": []}

    for (head_word_index, head_word) in enumerate(head_words):
        print(f'\n # Beginning for loop with "{head_word}"\n')
        if use_sample:
            with open(f'input/{language}/sample_{head_word}.html', 'r') as f:
                contents = f.read()
                parser.feed(contents)
                output_arr = parser.output_arr
                for lemma_object in output_arr:
                    lemma_object["lemma"] = head_word
                result.extend(output_arr)
                f.close()
        else:
            try:
                html_string = html_from_head_word(head_word, f"{head_word_index + 1} of {len(head_words)}")

                try:
                    started_at = datetime.now()
                    parser.reset_for_new_table()
                    parser.feed(html_string)
                    output_arr = parser.output_arr
                    parser.output_arr = []
                    parser.reset()

                    if output_arr:
                        print(f'\n{" " * 15}# SUCCESS Adding "{head_word}" output_arr to result.' "\n")
                        for lemma_object in output_arr:
                            lemma_object["lemma"] = head_word
                        result.extend(output_arr)
                    else:
                        print(f'\n#{" " * 45}Loaded and read html for "{head_word}" but FAILED to create output.\n')
                        rejected["loaded_and_read_html_but_failed_to_create_output"].append(head_word)


                except:
                    print(f'\n#{" " * 30}Loaded html for "{head_word}" but FAILED when reading it.\n')
                    rejected["loaded_html_but_failed_when_reading"].append(head_word)
                    parser.output_arr = []
                    output_arr = []
                    parser.reset()

            except:
                print(f'\n#{" " * 30}FAILED to even load html for "{head_word}".\n')
                rejected["failed_to_load_html"].append(head_word)

            delay_seconds = 1

            if datetime.now() < started_at + timedelta(seconds=delay_seconds):
                if datetime.now() < started_at + timedelta(seconds=delay_seconds / 2):
                    sleep(delay_seconds)
                else:
                    sleep(delay_seconds / 2)

    print(f'\n# Writing results".')

    if not no_temp_ids:
        for lemma_object in result:
            lemma_object["temp_id"] = f"{group_number}.{count}"
            count += 1

    write_output(result, filepaths["output"])
    write_output(rejected, filepaths["rejected"])

    if "truncated" in filepaths:
        def get_truncated(lemma_object):
            return {
                "lemma": lemma_object["lemma"],
                "tags": "xxxxxxxxx",
                "translations": lemma_object["translations"],
                "temp_id": str(lemma_object["temp_id"]),
                "gender": lemma_object["gender"],
            }

        truncated_result = [get_truncated(lemma_object) for lemma_object in result]
        write_output(truncated_result, filepaths["truncated"])
