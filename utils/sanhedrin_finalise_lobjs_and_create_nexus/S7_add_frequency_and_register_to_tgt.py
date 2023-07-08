import json
import os
import time

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q
from utils.postprocessing.common import finalise_lemma_objects, add_tags_and_topics_from_shorthand
from utils.scraping.Polish_dicts import shorthand_tag_refs
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    # # # # # #

    suffix = "TGT"
    input_filename = f"{wordtype}_batch_{batch}_{suffix}"
    src_input_filename = f"{wordtype}_batch_{batch}_SRC"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"
    src_input_path = f"{stem}{src_input_filename}"

    c.print_teal("input_path =     " + c.teal(input_path))
    c.print_teal("src_input_path = " + c.teal(src_input_path))
    c.print_teal("Output path will be the same as input.")
    c.print_teal("No tempsave files are used for this stage.")

    lobjs = []
    src_lobjs = []

    with open(input_path + ".json", "r") as f:
        lobjs = json.load(f)
        print("Loaded", len(lobjs), "lobjs.")
        f.close()

    with open(src_input_path + ".json", "r") as f:
        src_lobjs = json.load(f)
        print("Loaded", len(lobjs), "src_lobjs.")
        f.close()

    for lobj in lobjs:
        lobj["register"] = 0
        lobj["frequency"] = 0

        corresponding_src_lobjs = []

        for tran in lobj["»trans"]:
            for sl in src_lobjs:
                if sl["id"] == tran:
                    corresponding_src_lobjs.append(sl)

        if len(corresponding_src_lobjs) == 1:
            lobj["frequency"] = corresponding_src_lobjs[0]["frequency"]

        for corresponding_src_lobj in corresponding_src_lobjs:
            if corresponding_src_lobj["register"]:
                lobj["register"] = corresponding_src_lobj["register"]


    def get_freq(lobj):
        user_input = input(f'Enter frequency 1-5 for {c.blue(lobj["id"])} ')
        if user_input not in "12345":
            return get_freq(lobj)
        return int(user_input)


    lobjs_without_freq = [l for l in lobjs if not lobj["frequency"]]

    for lindex, lobj in enumerate(lobjs_without_freq):
        print(f"{lindex+1}/{len(lobjs_without_freq)}")
        lobj["frequency"] = get_freq(lobj)

    with open(input_path + ".json", "w") as outfile:
        print(f'Writing {len(lobjs)} results.')
        data_json = json.dumps(lobjs, indent=2, ensure_ascii=False)
        outfile.write(data_json)
        outfile.close()

    print("Completely done.")
