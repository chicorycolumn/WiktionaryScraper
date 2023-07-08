import json
import os
import time

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, get_freq
from utils.postprocessing.common import finalise_lemma_objects, add_tags_and_topics_from_shorthand
from utils.scraping.Polish_dicts import shorthand_tag_refs
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    # # # # # #

    input_filename = f"{wordtype}_batch_{batch}_TGT"
    src_input_filename = f"{wordtype}_batch_{batch}_SRC"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"
    # tempsave_path = f"{stem}{input_filename}_S8_tempsave"
    src_input_path = f"{stem}{src_input_filename}"

    c.print_teal("input_path =     " + c.teal(input_path))
    c.print_teal("src_input_path = " + c.teal(src_input_path))
    c.print_teal("No tempsave file is used in this stage.")
    # c.print_teal("tempsave_path = " + c.teal(tempsave_path))
    c.print_teal("Output path will be the same as input.")

    def save(data):
        print(f"📀 {'SAVING FINAL'}")

        _output_path = input_path

        with open(_output_path + ".json", "w") as outfile:
            print(f'Writing {len(data)} results.')
            data_json = json.dumps(data, indent=2, ensure_ascii=False)
            outfile.write(data_json)
            outfile.close()

    lobjs = []

    with open(input_path + ".json", "r") as f:
        lobjs = json.load(f)
        print("Loaded", len(lobjs), "lobjs.")
        f.close()

    sorted_lobjs = {}

    sorted_lobjs["F1"] = [l for l in lobjs if int(l["frequency"]) == 1]
    sorted_lobjs["F2"] = [l for l in lobjs if int(l["frequency"]) == 2]
    sorted_lobjs["F3"] = [l for l in lobjs if int(l["frequency"]) == 3]
    sorted_lobjs["F4"] = [l for l in lobjs if int(l["frequency"]) == 4]
    sorted_lobjs["F5"] = [l for l in lobjs if int(l["frequency"]) == 5]

    print("")
    for num in [1,2,3,4,5]:
        print(len(sorted_lobjs["F" + str(num)]), f"lobjs with frequency category {str(num)}.")

    user_input = input("Which frequency category do you want to check? 1-5 ")

    if user_input and user_input in "12345":
        freq_to_check = user_input
        lobjs_to_check = sorted_lobjs["F" + str(freq_to_check)]
        for lindex, lob in enumerate(lobjs_to_check):
            print(f"{lindex+1}/{len(lobjs_to_check)}")
            print(f'{c.purple(lob["lemma"])} {c.blue(lob["id"])}')
            user_input = get_freq(lob, f"{freq_to_check} OK?   Enter for yes   Or enter new frequency ", True)
            if user_input:
                lob["frequency"] = int(user_input)

    print("Completely done.")
    save(lobjs)
