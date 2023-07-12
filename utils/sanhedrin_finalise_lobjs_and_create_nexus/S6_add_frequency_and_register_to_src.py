import json
import os
import time

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, reg_refs
from utils.postprocessing.common import finalise_lemma_objects, add_tags_and_topics_from_shorthand
from utils.scraping.Polish_dicts import shorthand_tag_refs
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c, get_curried_save

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    # # # # # #

    input_filename = f"{wordtype}_batch_{batch}_SRC"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"
    save = get_curried_save(input_path, None)

    c.print_teal("input_path =     " + c.teal(input_path))
    c.print_teal("Output path will be the same as input.")
    c.print_teal("No tempsave files are used for this stage.")

    with open(input_path + ".json", "r") as f:
        src_lobjs = json.load(f)
        print("Loaded", len(src_lobjs), "source lobjs.")

        for src_lobj in src_lobjs:

            #  register
            #  0 = neutral
            #  1 = fancy
            #  6 = slang
            #  7 = insult
            #  8 = curseword

            freq = "X"
            for tag in src_lobj["tags"]:
                if tag.startswith("FREQ"):
                    freq = int(tag[4:])
                    src_lobj["tags"].remove(tag)
            if freq == "X":
                raise Exception(f'No frequency tag on "{src_lobj["id"]}"')

            register = 0

            for reg_ref in reg_refs:
                if reg_ref["tag"] in src_lobj["tags"]:
                    src_lobj["tags"].remove(reg_ref["tag"])
                    register = reg_ref["num"]

            src_lobj["frequency"] = freq
            src_lobj["register"] = register

        f.close()

    save(src_lobjs)

    print("Completely done.")
