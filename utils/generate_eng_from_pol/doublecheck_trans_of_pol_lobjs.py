import json
import os
import time
from copy import deepcopy

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.generate_eng_from_pol.tools import is_it_the_same_meaning, q, show1, user_validate_translations
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    input_filename = "adjectives_batch_1_is_groups_01_to_09"
    input_override = 0  # Only set True for dryruns
    # # # # # #

    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}.json"
    tempsave_path = f"{stem}tempsave_doublecheck_trans_of_pol_lobjs.json"
    output_path = f"{stem}{input_filename}_doublechecked.json"

    with open(tempsave_path, "r") as f:
        doublechecked_pol_lobjs = json.load(f)
        ids_of_done_so_far_pol_lobjs = [l["id"] for l in doublechecked_pol_lobjs]
        f.close()

    with open(input_path, "r") as f:
        pol_lobjs = json.load(f)
        print("Loaded", len(pol_lobjs), "polish lobjs.")

        for pol_lobj_index, pol_lobj in enumerate(pol_lobjs):

            print("")
            print("")
            print(f"{pol_lobj_index + 1}/{len(pol_lobjs)}")

            if pol_lobj["id"] not in ids_of_done_so_far_pol_lobjs:
                user_validate_translations(pol_lobj, doublechecked_pol_lobjs)
            else:
                print("already done")

        f.close()

        print("")
        print("Done all lobjs, so now doublechecked_pol_lobjs has length", len(doublechecked_pol_lobjs))

        doublechecked_pol_lobjs_json = json.dumps(doublechecked_pol_lobjs, indent=2, ensure_ascii=False)

        with open(output_path, "w") as outfile:
            outfile.write(doublechecked_pol_lobjs_json)

        print("Completely done.")
