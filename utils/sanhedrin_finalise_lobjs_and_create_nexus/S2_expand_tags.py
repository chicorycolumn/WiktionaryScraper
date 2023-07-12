import json
import os
import time

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q
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

    failed_flags = False
    with open(input_path + ".json", "r") as f:
        src_lobjs = json.load(f)
        print("Loaded", len(src_lobjs), "source lobjs.")

        for src_lobj in src_lobjs:
            for flag_char in "🚩🏁⛳":
                if not failed_flags and flag_char in src_lobj["id"] or flag_char in src_lobj["tags"]:
                    failed_flags = True

        f.close()

    if failed_flags:
        c.print_red("Unresolved flags 🚩🏁⛳ from " + input_path)
        c.print_red("See instructions.txt step 3.")
    else:
        with open(input_path + ".json", "r") as f:
            src_lobjs = json.load(f)
            print("Loaded", len(src_lobjs), "source lobjs.")

        for src_lobj in src_lobjs:
            if type(src_lobj["tags"]) == str:
                print("")
                print(q(src_lobj["id"]))
                print(q(src_lobj["tags"]), "BECOMES")
                add_tags_and_topics_from_shorthand(src_lobj, shorthand_tag_refs, wordtype)
                print("TAGS:", src_lobj["tags"])
                print("TOPICS:", src_lobj["topics"])

        f.close()

    save(src_lobjs)

    print("Completely done.")
