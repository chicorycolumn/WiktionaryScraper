import json
import os
import time

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.generate_eng_from_pol.tools import is_it_the_same_meaning, q
from utils.postprocessing.common import finalise_lemma_objects, add_tags_and_topics_from_shorthand
from utils.scraping.Polish_dicts import shorthand_tag_refs
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    # # # # # #

    input_filename = f"{wordtype}_batch_{batch}_SAN"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"

    c.print_teal("input_path =     " + c.teal(input_path))
    c.print_teal("Output path will be the same as input.")
    c.print_teal("No tempsave files are used for this stage.")

    failed_flags = False
    with open(input_path + ".json", "r") as f:
        pol_lobjs = json.load(f)
        print("Loaded", len(pol_lobjs), "polish lobjs.")

        for pol_lobj in pol_lobjs:
            for flag_char in "🚩🏁⛳":
                if not failed_flags and flag_char in pol_lobj["id"] or flag_char in pol_lobj["tags"]:
                    failed_flags = True

        f.close()

    if failed_flags:
        c.print_red("Unresolved flags 🚩🏁⛳ from " + input_path)
        c.print_red("See instructions.txt step 3.")
    else:
        with open(input_path + ".json", "r") as f:
            pol_lobjs = json.load(f)
            print("Loaded", len(pol_lobjs), "polish lobjs.")

        for pol_lobj in pol_lobjs:
            if type(pol_lobj["tags"]) == str:
                print("")
                print(q(pol_lobj["id"]))
                print(q(pol_lobj["tags"]), "BECOMES")
                add_tags_and_topics_from_shorthand(pol_lobj, shorthand_tag_refs, wordtype)
                print("TAGS:", pol_lobj["tags"])
                print("TOPICS:", pol_lobj["topics"])

        f.close()

    with open(input_path + ".json", "w") as outfile:
        data_json = json.dumps(pol_lobjs, indent=2, ensure_ascii=False)
        outfile.write(data_json)
        outfile.close()

    print("Completely done.")
