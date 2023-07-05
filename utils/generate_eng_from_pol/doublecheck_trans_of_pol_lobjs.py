import json
import os
import time

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.generate_eng_from_pol.tools import is_it_the_same_meaning, q
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing


if __name__ == '__main__':
    
    # # # # # #
    wordtype = "adj"
    input_filename = "adjectives_batch_1_is_groups_01_to_09"
    input_override = 0  # Only set True for dryruns
    # # # # # #

    stem = "./../output_saved/batches/"
    input_path = f"{stem}{input_filename}.json"
    output_path = f"{stem}{input_filename}_doublechecked.json"
    doublechecked_pol_lobjs = []

    with open(input_path, "r") as f:
        pol_lobjs = json.load(f)
        print("Loaded", len(pol_lobjs), "polish lobjs.")

        for pol_lobj_index, pol_lobj in enumerate(pol_lobjs):

            print("")
            print("")
            print("     Starting pol_lobj", q(pol_lobj["id"]), f"{pol_lobj_index + 1}/{len(pol_lobjs)}")
            print("")
            print("")
            print(pol_lobj["translations"]["ENG"])

            input_num = input("...")

            if input == 1:
                print("one")
            elif input == 2:
                print("two")
            elif input == 3:
                print("three")
            elif input == 4:
                print("four")
            elif input == 5:
                print("five")

            doublechecked_pol_lobjs.append(pol_lobj)

        f.close()

    print("")
    print("Done all lobjs, so now doublechecked_pol_lobjs has length", len(doublechecked_pol_lobjs))

    doublechecked_pol_lobjs_json = json.dumps(doublechecked_pol_lobjs, indent=2, ensure_ascii=False)

    with open(output_path, "w") as outfile:
        outfile.write(doublechecked_pol_lobjs_json)

    print("Completely done.")

    # for root, dirs, files in os.walk(path):
    #     print(files)
    #     for file in files:
    #         with open(f'{path}/{file}', "r") as f:
    #             loaded = json.load(f)
    #             for lobj in loaded:
    #                 # if lobj["gender"] == "m1":
    #                 #     m1_lobjs.append(lobj["id"])
    #                 if lobj["id"].split("-")[1] == "nco":
    #                     print(lobj["id"].split("-")[3])
    #             f.close()