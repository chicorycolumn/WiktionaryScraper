from parsers.Polish_adjective_parser import PolishAdjectiveParser
from parsers.Polish_noun_parser import PolishNounParser
from parsers.Polish_verb_parser import PolishVerbParser

from datetime import timedelta, datetime
from time import sleep
import json

from utils.general.common import write_output
from utils.postprocessing.Polish import generate_adjective
from utils.scraping.Polish import minimise_inflections
from utils.scraping.common import html_from_head_word


def scrape_word_data(
        language: str,
        head_words: dict,
        wordtype: str,
        use_sample: bool = False,
        filepaths: object = {},
        group_number: int = int(str(datetime.now())[-3:]),
        no_temp_ids: bool = False,
        skip_scraping: bool = False,
):
    if wordtype == "adjectives":
        parser = PolishAdjectiveParser(convert_charrefs=False)
    elif wordtype == "nouns":
        parser = PolishNounParser(convert_charrefs=False)
    elif wordtype == "verbs":
        parser = PolishVerbParser(convert_charrefs=False)

    if not filepaths:
        filepaths = {
            "output": f"output_{wordtype}_{group_number}",
            "rejected": f"rejected_{wordtype}_{group_number}",
            "truncated": f"truncated_{wordtype}_{group_number}",
        }

    if skip_scraping:
        with open(f"output/output_{wordtype}_{group_number}_scraped.json", "r") as f:
            result = json.load(f)
            f.close()
    else:
        print(f'## Starting, given {len(head_words)} words.')

        if not head_words:
            head_words = ["małpa"]

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
        write_output(result, f'{filepaths["output"]}_scraped')

    if wordtype == "adjectives":
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