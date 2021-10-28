from datetime import timedelta
from time import sleep

from scraper_utils.Polish import minimise_inflections
from scraper_utils.common import *
from semimanual_utils.Polish import generate_adjective

shorthand_tag_refs = {
    "k": {
        "tags": ["colour"],
        "topics": ["basic"],
    },
    "z": {
        "tags": ["dimensions"],
        "topics": ["basic"],
    },

    # # # # # # # # # # #

    "u": {
        "tags": ["uncountable"],
        "topics": [],
    },
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
        "tags": ["household object", "h"],
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


def expand_tags_and_topics(group_number, wordtype):
    res_arr = []

    with open(f"output_saved/untruncated_{wordtype}_{group_number}.json", "r") as f:
        untruncated_lobjs = json.load(f)
        f.close()

    for lemma_object in untruncated_lobjs:
        add_tags_and_topics_from_shorthand(lemma_object, shorthand_tag_refs)
        res_arr.append(lemma_object)

    return res_arr


def recursively_expand_tags(input_stags: list, ref: object):
    output_tags = []

    def ret_inner(input_tags: list):
        for tag in input_tags:
            if tag in ref:
                ret_inner(ref[tag]["tags"])
            elif tag not in output_tags:
                output_tags.append(tag)

    ret_inner(input_stags)
    return output_tags


def add_tags_and_topics_from_shorthand(lemma_object: object, ref: object):
    shorthand_tags = lemma_object["tags"].split(",")

    tags = recursively_expand_tags(shorthand_tags, ref)

    topics = []
    for stag in shorthand_tags:
        if stag in ref:
            for topic in ref[stag]["topics"]:
                if topic not in topics:
                    topics.append(topic)

    tags.sort()
    topics.sort()

    lemma_object["tags"] = tags
    lemma_object["topics"] = topics


def finalise_lemma_objects(group_number, wordtype):
    untruncate_lemma_objects(group_number, wordtype)
    res_arr = expand_tags_and_topics(group_number, wordtype)
    write_output(res_arr, f"finished_{wordtype}_{group_number}", f"output_saved/{wordtype}")


def untruncate_lemma_objects(group_number, wordtype):
    res_arr = []

    with open(f"output_saved/output_{wordtype}_{group_number}.json", "r") as f:
        lobjs_long = json.load(f)
        f.close()
    with open(f"output_saved/truncated_{wordtype}_{group_number}.json", "r") as f:
        lobjs_truncated = json.load(f)
        f.close()

    for lemma_object in lobjs_truncated:
        lemma_object_long = [lol for lol in lobjs_long if lol["temp_id"] == get_base_id(lemma_object["temp_id"])][0]

        for key in lemma_object_long:
            if key not in lemma_object:
                lemma_object[key] = lemma_object_long[key]

        res_arr.append(lemma_object)

    write_output(res_arr, f"untruncated_{wordtype}_{group_number}", f"output_saved")


def scrape_word_data(
        parser,
        language: str,
        head_words: dict,
        wordtype: str,
        use_sample: bool,
        filepaths: object = {},
        group_number: int = int(str(datetime.now())[-3:]),
        no_temp_ids: bool = False,
):
    print(f'## Starting, given {len(head_words)} words.')

    if not head_words:
        head_words = ["małpa"]

    if not filepaths:
        filepaths = {
            "output": f"output_{wordtype}_{group_number}",
            "rejected": f"rejected_{wordtype}_{group_number}",
            "truncated": f"truncated_{wordtype}_{group_number}",
        }

    count = 1
    result = []
    rejected = {"failed_to_load_html": [], "loaded_html_but_failed_when_reading": [],
                "loaded_and_read_html_but_failed_to_create_output": []}

    for (head_word_index, head_word) in enumerate(head_words):
        print(f'\n # Beginning for loop with "{head_word}"\n')

        parser.reset()

        def add_output_arr_to_result(output_arr):
            if output_arr:
                print(f'\n{" " * 15}# SUCCESS Adding "{head_word}" output_arr to result.' "\n")
                for lemma_object in output_arr:
                    lemma_object["lemma"] = head_word
                result.extend(output_arr)
            else:
                print(f'\n#{" " * 45}Loaded and read html for "{head_word}" but FAILED to create output.\n')
                rejected["loaded_and_read_html_but_failed_to_create_output"].append(head_word)

        if use_sample:
            with open(f'input/{language}/{wordtype}/sample_{head_word}.html', 'r') as f:
                contents = f.read()
                parser.feed(contents)
                output_arr = parser.output_arr
                add_output_arr_to_result(output_arr)
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
                    add_output_arr_to_result(output_arr)

                except:
                    print(f'\n#{" " * 30}Loaded html for "{head_word}" but FAILED when reading it.\n')
                    rejected["loaded_html_but_failed_when_reading"].append(head_word)

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
            lemma_object_copy = {}
            lemma_object_copy["temp_id"] = f"{group_number}.{count}"
            count += 1
            for key, value in lemma_object.items():
                lemma_object_copy[key] = value
            lemma_object_keys = [key for key in lemma_object]
            for key in lemma_object_keys:
                lemma_object.pop(key)
            for key, value in lemma_object_copy.items():
                lemma_object[key] = value

    write_output(rejected, filepaths["rejected"])

    if wordtype == "adjectives":
        write_output(result, f'{filepaths["output"]}_protoadjective')
        generated_adjectives = [generate_adjective(
            lemma=protoadjective["lemma"],
            translations_list=protoadjective["translations"],
            comparative_type=protoadjective["comparative_type"],
            pluvirnom_lemma=protoadjective["pluvirnom_lemma"] if "pluvirnom_lemma" in protoadjective else [],
            adverb=protoadjective["adverb"] if "adverb" in protoadjective else [],
            comparative=protoadjective["comparative"] if "comparative" in protoadjective else [],
            lemma_object=protoadjective
        ) for protoadjective in result]
        result = generated_adjectives
    elif wordtype == "verbs":
        write_output(result, f'{filepaths["output"]}_fullverb')
        minimised_verbs = [minimise_inflections(fullverb) for fullverb in result]
        result = minimised_verbs

    write_output(result, filepaths["output"])

    if "truncated" in filepaths:
        def get_truncated(lemma_object):
            truncated_lemma_object = {
                "lemma": lemma_object["lemma"],
                "tags": "xxxxxxxxx",
                "translations": lemma_object["translations"],
                "temp_id": str(lemma_object["temp_id"]),
            }
            if wordtype == "nouns":
                truncated_lemma_object["gender"] = lemma_object["gender"]
            return truncated_lemma_object

        truncated_result = [get_truncated(lemma_object) for lemma_object in result]
        write_output(truncated_result, filepaths["truncated"])

    print(f'\n## Scraped at "{filepaths["output"]}" for {len(head_words)} words:', head_words)
