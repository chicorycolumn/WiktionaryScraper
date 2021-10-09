import json
import urllib.request as urllib2
import urllib as urllib
from datetime import datetime, timedelta
from time import sleep
import re
from scraper_utils.common import *


def add_tags_from_shorthand():
    pass


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
    rejected = {"failed_to_load_html": [], "loaded_html_but_failed_when_reading": [], "loaded_and_read_html_but_failed_to_create_output": []}

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
                html_string = html_from_head_word(head_word, f"{head_word_index+1} of {len(head_words)}")

                try:
                    started_at = datetime.now()
                    parser.reset_for_new_table()
                    parser.feed(html_string)
                    output_arr = parser.output_arr
                    parser.output_arr = []
                    parser.reset()

                    if output_arr:
                        print(f'\n{" "*15}# SUCCESS Adding "{head_word}" output_arr to result.' "\n")
                        for lemma_object in output_arr:
                            lemma_object["lemma"] = head_word
                        result.extend(output_arr)
                    else:
                        print(f'\n#{" "*45}Loaded and read html for "{head_word}" but FAILED to create output.\n')
                        rejected["loaded_and_read_html_but_failed_to_create_output"].append(head_word)


                except:
                    print(f'\n#{" "*30}Loaded html for "{head_word}" but FAILED when reading it.\n')
                    rejected["loaded_html_but_failed_when_reading"].append(head_word)
                    parser.output_arr = []
                    output_arr = []
                    parser.reset()

            except:
                print(f'\n#{" "*30}FAILED to even load html for "{head_word}".\n')
                rejected["failed_to_load_html"].append(head_word)

            delay_seconds = 1

            if datetime.now() < started_at + timedelta(seconds=delay_seconds):
                if datetime.now() < started_at + timedelta(seconds=delay_seconds/2):
                    sleep(delay_seconds)
                else:
                    sleep(delay_seconds/2)


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