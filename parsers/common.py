from datetime import timedelta, datetime
from time import sleep
import json
import re

from parsers.Polish_adjective_parser import PolishAdjectiveParser
from parsers.Polish_noun_parser import PolishNounParser
from parsers.Polish_verb_parser import PolishVerbParser

from utils.general.common import write_output, write_todo, get_existing_lobjs
from utils.postprocessing.Polish import generate_adjective
from utils.scraping.Polish import minimise_inflections
from utils.scraping.common import html_from_head_word


def add_output_arr_to_result(output_arr, head_word, result, rejected):
    if output_arr:
        print(f'\n{" " * 15}# SUCCESS Adding "{head_word}" output_arr to result.' "\n")
        for lemma_object in output_arr:
            lemma_object["lemma"] = head_word
        result.extend(output_arr)
    else:
        print(f'\n#{" " * 45}Loaded and read html for "{head_word}" but FAILED to create output.\n')
        rejected["loaded_and_read_html_but_failed_to_create_output"].append(head_word)


def trigger_parser(head_words_raw, parser, use_sample, language, wordtype, result, rejected, extra_lemmas_to_parse, test_only_boolean_override_check_existing=False):
    if not test_only_boolean_override_check_existing:
        already_parsed_headwords = get_existing_lobjs(wordtype, lemmas_only=True)
        head_words = []
        headwords_not_to_parse = []

        for headword in head_words_raw:
            if headword in already_parsed_headwords:
                headwords_not_to_parse.append(headword)
            else:
                head_words.append(headword)

        if headwords_not_to_parse:
            if "already_existing" not in rejected:
                rejected["already_existing"] = []
            rejected["already_existing"].extend(headwords_not_to_parse)
    else:
        write_todo(f'Remember to set test_only_boolean_override_check_existing back to False.')
        head_words = head_words_raw
        if len(head_words) > 10:
            write_todo(f'Actually, I refuse to override rejection of already existing headwords for more than ten.')
            return

    for (head_word_index, head_word) in enumerate(head_words):
        print(f'\n # Beginning for loop with "{head_word}"\n')

        parser.reset()

        if use_sample:
            with open(f'input/{language}/{wordtype}/sample_{head_word}.html', 'r') as f:
                contents = f.read()
                parser.feed(contents)
                output_arr = parser.output_arr
                add_output_arr_to_result(output_arr, head_word, result, rejected)
                f.close()
        else:
            started_at = datetime.now()

            try:
                html_string = html_from_head_word(head_word, head_word_index, len(head_words))

                try:
                    started_at = datetime.now()
                    parser.reset_for_new_table()
                    parser.feed(html_string)
                    output_arr = parser.output_arr
                    parser.output_arr = []
                    add_output_arr_to_result(output_arr, head_word, result, rejected)

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

    for lobj in result:
        if "extra" in lobj:
            extra_lemmas_object = {"lemma": lobj["lemma"], "extra_lemmas": [], "lemma_objects": []}

            if "otherShapes" in lobj["extra"]:
                for other_shapes_key, other_shapes_values in lobj["extra"]["otherShapes"].items():
                    for other_shapes_value in other_shapes_values:
                        if "się" in other_shapes_value:
                            other_shapes_value = " ".join([s for s in other_shapes_value.split(" ") if s != "się"])
                        extra_lemmas_object["extra_lemmas"].append(other_shapes_value)

            if wordtype == "adjectives":
                for nym in ["synonyms", "antonyms"]:
                    if nym in lobj["extra"]:
                        extra_lemmas_object["extra_lemmas"].extend(lobj["extra"][nym])

            extra_lemmas_to_parse.append(extra_lemmas_object)


def reorder_lemma_objects_in_result(result, extra_lemmas_objs):
    result_length = len(result)

    indexes = [i for i in range(0, len(result))]
    indexes.reverse()

    for index in indexes:
        lobj = result[index]
        for extra_lemmas_obj in extra_lemmas_objs:
            if lobj["lemma"] in extra_lemmas_obj["extra_lemmas"] + [extra_lemmas_obj["lemma"]]:
                extra_lemmas_obj["lemma_objects"].append(result.pop(index))
                break

    ordered_result = []

    for extra_lemmas_obj in extra_lemmas_objs:
        extra_lemmas_obj["lemma_objects"].reverse()
        for lobj in extra_lemmas_obj["lemma_objects"]:
            ordered_result.append(lobj)
    for lobj in result:
        ordered_result.append(lobj)

    if result_length != len(ordered_result):
        raise Exception(f'ERR 530: Failure in reorder_lemma_objects_in_result. Input had {result_length} lobjs but output {len(ordered_result)} and should be the same.')

    return ordered_result


def scrape_word_data(
        language: str,
        head_words: dict,
        wordtype: str,
        use_sample: bool = False,
        filepaths: object = {},
        group_number: int = int(str(datetime.now())[-3:]),
        no_temp_ids: bool = False,
        skip_scraping: bool = False,
        skip_extras: bool = False,
        test_only_boolean_override_check_existing = False
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

        extra_lemmas_objs = []

        trigger_parser(head_words, parser, use_sample, language, wordtype, result, rejected, extra_lemmas_objs, test_only_boolean_override_check_existing=test_only_boolean_override_check_existing)

        existing_lemmas = get_existing_lobjs(wordtype, lemmas_only=True)

        extra = []
        for extra_lemmas_obj in extra_lemmas_objs:
            for el in extra_lemmas_obj["extra_lemmas"]:
                if el not in head_words + existing_lemmas:
                    extra.append(el.lower())

        extra = list(set(extra))

        if extra and not skip_extras:
            if wordtype in ["verbs", "adjectives"]:
                print(f"# There are {len(extra)} extra headwords now after parsing the original headwords:", extra)
                extra_lemmas_objs_2 = []
                trigger_parser(extra, parser, use_sample, language, wordtype, result, rejected, extra_lemmas_objs_2, test_only_boolean_override_check_existing=test_only_boolean_override_check_existing)

                extra_2 = []
                for extra_lemmas_obj in extra_lemmas_objs_2:
                    for el in extra_lemmas_obj["extra_lemmas"]:
                        if el not in head_words + extra + existing_lemmas:
                            extra_2.append(el.lower())

                extra_2 = list(set(extra_2))

                if extra_2:
                    write_todo(f'There are {len(extra_2)} doubly extra headwords, they have not been parsed: {extra_2}')
            else:
                write_todo(f'Want to parse any of {len(extra)} extra lemmas? (I did not because of wordtype) {extra}')

        print(f'\n# Writing results".')

        result = reorder_lemma_objects_in_result([el for el in result if el], extra_lemmas_objs)

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
        result_filtered = []

        for fullverb in result:
            if "infinitive" not in fullverb["inflections"]:
                write_todo(f'"{fullverb["lemma"]}" has no infinitive. Kicking it out.')
            else:
                result_filtered.append(fullverb)

        result = [minimise_inflections(fullverb) for fullverb in result_filtered]

    write_output(result, filepaths["output"])

    another_round_of_potential_extra_lemmas_to_parse = []
    for lobj in result:
        if "translations_additional" in lobj:
            for ta in lobj["translations_additional"]:
                if ta not in head_words + existing_lemmas and bool(re.search(r"^[a-zA-Z]+$", ta)):
                    another_round_of_potential_extra_lemmas_to_parse.append(ta)

    another_round_of_potential_extra_lemmas_to_parse = list(set(another_round_of_potential_extra_lemmas_to_parse))

    if another_round_of_potential_extra_lemmas_to_parse:
        write_todo(f'Want to parse any (if they are {language}) of {len(another_round_of_potential_extra_lemmas_to_parse)}'
                   f' translations_additional lemmas? (I did not): {another_round_of_potential_extra_lemmas_to_parse}')

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

        truncated_result = [get_truncated(lemma_object) for lemma_object in [el for el in result if el]]
        write_output(truncated_result, filepaths["truncated"])

    print(f'\n## Scraped at "{filepaths["output"]}" for {len(head_words)} words:', head_words)
