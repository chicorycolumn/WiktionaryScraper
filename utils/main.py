import json
import os

from input.Polish.nouns.head_words import input as nouns
from input.Polish.adjectives.head_words import input as adjectives
from input.Polish.verbs.head_words import input as verbs
from parsers.common import scrape_word_data
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from input.Polish.adjectives.head_words import input

#
#
# This main.py is just for checking lemma objects.
#
#

if __name__ == '__main__':
    path = "./../output_saved/batches/adjectives_batch_1_is_groups_01_to_09.json"

    with open(f'{path}', "r") as f:
        loaded = json.load(f)
        print(len(loaded))
        for lobj in loaded:
            if "adverb" in lobj:
                lobj.pop("adverb", None)
        f.close()
    print("swde")

    json_object = json.dumps(loaded, indent=2, ensure_ascii=False)

    with open(path, "w") as outfile:
        outfile.write(json_object)


    # wordtype = "n"
    #
    # for long_wordtype in ["nouns", "verbs", "adjectives"]:
    #     if wordtype[0] == long_wordtype[0]:
    #         wordtype = long_wordtype
    # path = f"./../output_saved/{wordtype}"
    #
    # npe_lobjs = []
    # m1_lobjs = []
    #
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
    # print("swde")
