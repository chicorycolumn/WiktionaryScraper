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
    start_id_number = 1
    suffix = "SRC"
    # # # # # #

    input_filename = f"{wordtype}_batch_{batch}_{suffix}"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"

    c.print_teal("input_path =     " + c.teal(input_path))
    c.print_teal("Output path will be the same as input.")
    c.print_teal("No tempsave files are used for this stage.")
    c.print_teal("ID numbers for lobjs will start from " + str(start_id_number))

    with open(input_path + ".json", "r") as f:
        src_lobjs = json.load(f)
        print("Loaded", len(src_lobjs), "source lobjs.")

        res = []

        for src_lobj in src_lobjs:
            new_id_number = "0000" + str(start_id_number)
            new_id_number = new_id_number[-4:]

            id_split = src_lobj["id"].split("-")
            id_split[2] = str(new_id_number)
            new_id = "-".join(id_split)

            src_lobj["id"] = new_id
            start_id_number += 1

        f.close()

    with open(input_path + ".json", "w") as outfile:
        print(f'Writing {len(src_lobjs)} results.')
        data_json = json.dumps(src_lobjs, indent=2, ensure_ascii=False)
        outfile.write(data_json)
        outfile.close()

    print("Completely done.")
