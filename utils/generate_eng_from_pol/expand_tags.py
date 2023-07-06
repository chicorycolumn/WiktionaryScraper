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
    # # # # # #

    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}.json"

    with open(input_path, "r") as f:
        pol_lobjs = json.load(f)
        print("Loaded", len(pol_lobjs), "polish lobjs.")

        res = []

        for pol_lobj in pol_lobjs:
            if type(pol_lobj["tags"]) == str:
                print("")
                print(q(pol_lobj["id"]))
                print(q(pol_lobj["tags"]), "BECOMES")
                add_tags_and_topics_from_shorthand(pol_lobj, shorthand_tag_refs, wordtype)
                print("TAGS:", pol_lobj["tags"])
                print("TOPICS:", pol_lobj["topics"])
            res.append(pol_lobj)

        f.close()

    with open(input_path, "w") as outfile:
        res_json = json.dumps(res, indent=2, ensure_ascii=False)
        outfile.write(res_json)
        outfile.close()

    print("Completely done.")
