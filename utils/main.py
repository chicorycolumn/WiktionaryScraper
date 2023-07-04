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

        all_new_eng_lobjs = []
        new_nexus_objs = []
        num = 1
        other_num = 1

        for pol_lobj in loaded:

            new_eng_lobjs = []

            for t in pol_lobj["translations"]["ENG"]:
                print(t)

                new_t = t

                for l in all_new_eng_lobjs:
                    if l["id"].split("-")[-1] == t:
                        new_t += "(þ)"

                new_id = f"eng-adj-{str(num).zfill(4)}-{new_t}"

                new_eng_lobj = {
                    "lemma": t,
                    "id": new_id,
                    "inflections": {
                        "simple": t,
                        "comparative": None,
                        "superlative": None,
                        "adverb": None
                    }
                }

                new_eng_lobjs.append(new_eng_lobj)

                num = num + 1

            new_nexus_obj = {
                "key": f"adj-{str(other_num).zfill(4)}-{new_eng_lobjs[0]['id'].split('-')[-1]}",
                "traductions": {
                  "SPA": [],
                  "ENG": [limmy["id"] for limmy in new_eng_lobjs],
                  "POL": [pol_lobj["id"]]
                },
                "papers": pol_lobj["tags"],
                "topics": pol_lobj["topics"]
            }

            new_nexus_objs.append(new_nexus_obj)
            all_new_eng_lobjs.extend(new_eng_lobjs)

            other_num = other_num + 1

        f.close()

    all_new_eng_lobjs_json = json.dumps(all_new_eng_lobjs, indent=2, ensure_ascii=False)
    with open("./../output_saved/batches/adjectives_batch_1_is_groups_01_to_09_ENG.json", "w") as outfile:
        outfile.write(all_new_eng_lobjs_json)

    new_nexus_objs_json = json.dumps(new_nexus_objs, indent=2, ensure_ascii=False)
    with open("./../output_saved/batches/adjectives_batch_1_is_groups_01_to_09_NEXUS.json", "w") as outfile:
        outfile.write(new_nexus_objs_json)

    print("swde")

    # json_object = json.dumps(loaded, indent=2, ensure_ascii=False)
    #
    # with open(path, "w") as outfile:
    #     outfile.write(json_object)

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
