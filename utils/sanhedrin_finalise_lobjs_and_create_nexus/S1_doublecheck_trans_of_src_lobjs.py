import json
import os
import time
from copy import deepcopy

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, show1, user_validate_translations
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c, get_curried_save

if __name__ == '__main__':

    # # # # # #
    wordtype = "nco"
    batch = "01"
    target_lang = "ENG"
    only_run_for_this_many_lobjs = 0  # Only set to integer for testing purposes.
    # # # # # #

    filename = f"{wordtype}_batch_{batch}_SRC"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{filename}_original"
    output_path = f"{stem}{filename}"
    tempsave_path = output_path + "_S1_tempsave"
    save = get_curried_save(output_path, tempsave_path)

    c.print_teal("input_path    =     " + c.teal(input_path))
    c.print_teal("output_path   =     " + c.teal(output_path))
    c.print_teal("tempsave_path =     " + c.teal(tempsave_path))

    doublechecked_src_lobjs = []

    if os.path.isfile(tempsave_path + ".json"):
        with open(tempsave_path + ".json", "r") as f:
            doublechecked_src_lobjs = json.load(f)
            c.print_teal("Loaded " + str(len(doublechecked_src_lobjs)) + " items from tempsave.")
            f.close()
    else:
        c.print_teal("No tempsave_path file found, I assume you're at the start of this batch?")

    ready = True
    if len(doublechecked_src_lobjs):
        id_of_last_done_src_lobj = doublechecked_src_lobjs[-1]["id"]
        ready = False

    with open(input_path + ".json", "r") as f:
        src_lobjs = json.load(f)
        print("Loaded", len(src_lobjs), "source lobjs.")

        if only_run_for_this_many_lobjs:
            src_lobjs = src_lobjs[:only_run_for_this_many_lobjs]
            c.print_bold("BUT FOR TESTING LET'S JUST SAY " + str(len(src_lobjs)))

        for src_lobj_index, src_lobj in enumerate(src_lobjs):

            print("")
            print("")
            print(f"{src_lobj_index + 1}/{len(src_lobjs)}")

            if ready:
                user_validate_translations(src_lobj, doublechecked_src_lobjs, save, target_lang)
            else:
                if not ready and src_lobj["id"] == id_of_last_done_src_lobj:
                    ready = True
                else:
                    print("Already done")

        f.close()

    if ready:
        print("")
        print("Done all lobjs, so now doublechecked_src_lobjs has length", len(doublechecked_src_lobjs))

        save(doublechecked_src_lobjs)

        print("Completely done.")
