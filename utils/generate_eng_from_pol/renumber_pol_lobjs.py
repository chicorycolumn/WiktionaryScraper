import json
import os
import time

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.generate_eng_from_pol.tools import is_it_the_same_meaning, q
from utils.postprocessing.common import finalise_lemma_objects, add_tags_and_topics_from_shorthand
from utils.scraping.Polish_dicts import shorthand_tag_refs
from utils.scraping.common import check_rescraped_against_existing

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    input_filename = "adjectives_batch_1_is_groups_01_to_09_doublechecked"
    start_id_number = 1
    # # # # # #

    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}.json"

    with open(input_path, "r") as f:
        pol_lobjs = json.load(f)
        print("Loaded", len(pol_lobjs), "polish lobjs.")

        res = []

        for pol_lobj in pol_lobjs:

            id_split = pol_lobj["id"].split("-")

            new_id_number = "0000" + str(start_id_number)
            new_id_number = new_id_number[-4:]

            id_split[2] = str(new_id_number)

            new_id = "-".join(id_split)

            pol_lobj["id"] = new_id

            res.append(pol_lobj)

            start_id_number += 1

        f.close()

    with open(input_path, "w") as outfile:
        res_json = json.dumps(res, indent=2, ensure_ascii=False)
        outfile.write(res_json)
        outfile.close()

    print("Completely done.")
