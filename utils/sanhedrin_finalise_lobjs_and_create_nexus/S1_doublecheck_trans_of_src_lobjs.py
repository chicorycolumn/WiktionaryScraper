import json
import os
import time
from copy import deepcopy

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, show1, user_validate_translations
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    target_lang = "ENG"
    override_slice = 0  # Only set to integer if you want to test with that many lobjs
    # # # # # #

    input_filename = f"{wordtype}_batch_{batch}"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"
    output_path = input_path + "_SRC"
    tempsave_path = output_path + "_S1_tempsave"

    c.print_teal("input_path    =     " + c.teal(input_path))
    c.print_teal("output_path   =     " + c.teal(output_path))
    c.print_teal("tempsave_path =     " + c.teal(tempsave_path))


    def save(data, temp: bool = False):
        print(f"📀 {'SAVING PROGRESS' if temp else 'SAVING FINAL'}")

        _output_path = tempsave_path if temp else output_path

        with open(_output_path + ".json", "w") as outfile:
            data_json = json.dumps(data, indent=2, ensure_ascii=False)
            outfile.write(data_json)
            outfile.close()


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

        if override_slice:
            src_lobjs = src_lobjs[:override_slice]
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
