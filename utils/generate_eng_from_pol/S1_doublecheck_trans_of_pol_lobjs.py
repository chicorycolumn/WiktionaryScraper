import json
import os
import time
from copy import deepcopy

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.generate_eng_from_pol.tools import is_it_the_same_meaning, q, show1, user_validate_translations
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    override_slice = 0  # Only set to integer if you want to test with that many lobjs
    # # # # # #

    input_filename = f"{wordtype}_batch_{batch}"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"
    output_path = input_path + "_SAN"
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


    doublechecked_pol_lobjs = []

    if os.path.isfile(tempsave_path + ".json"):
        with open(tempsave_path + ".json", "r") as f:
            doublechecked_pol_lobjs = json.load(f)
            c.print_teal("Loaded " + str(len(doublechecked_pol_lobjs)) + " items from tempsave.")
            f.close()
    else:
        c.print_teal("No tempsave_path file found, I assume you're at the start of this batch?")

    ready = True
    if len(doublechecked_pol_lobjs):
        id_of_last_done_pol_lobj = doublechecked_pol_lobjs[-1]["id"]
        ready = False

    with open(input_path + ".json", "r") as f:
        pol_lobjs = json.load(f)
        print("Loaded", len(pol_lobjs), "polish lobjs.")

        if override_slice:
            pol_lobjs = pol_lobjs[:override_slice]
            c.print_bold("BUT FOR TESTING LET'S JUST SAY " + str(len(pol_lobjs)))

        for pol_lobj_index, pol_lobj in enumerate(pol_lobjs):

            print("")
            print("")
            print(f"{pol_lobj_index + 1}/{len(pol_lobjs)}")

            if ready:
                user_validate_translations(pol_lobj, doublechecked_pol_lobjs, save)
            else:
                if not ready and pol_lobj["id"] == id_of_last_done_pol_lobj:
                    ready = True
                else:
                    print("Already done")

        f.close()

    if ready:
        print("")
        print("Done all lobjs, so now doublechecked_pol_lobjs has length", len(doublechecked_pol_lobjs))

        save(doublechecked_pol_lobjs)

        print("Completely done.")
