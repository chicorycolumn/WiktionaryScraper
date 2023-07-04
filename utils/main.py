import json
import os

from input.Polish.nouns.head_words import input as nouns
from input.Polish.adjectives.head_words import input as adjectives
from input.Polish.verbs.head_words import input as verbs
from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from input.Polish.adjectives.head_words import input

#
#
# This main.py is just for checking lemma objects.
#
#


def is_it_the_same_meaning(lobj_1, lobj_2):
    a_topics = lobj_1["topics"]
    b_topics = lobj_2["topics"]
    a_tags = [y for y in lobj_1["tags"] if y[:4] != "FREQ"]
    b_tags = [y for y in lobj_2["tags"] if y[:4] != "FREQ"]

    if "extra" in lobj_2:
        if "synonyms" in lobj_2["extra"]:
            if lobj_1["lemma"] in lobj_2["extra"]["synonyms"]:
                return True

    if "extra" in lobj_1:
        if "synonyms" in lobj_1["extra"]:
            if lobj_2["lemma"] in lobj_1["extra"]["synonyms"]:
                return True

    topics_match = False
    tags_match = False

    if not len(a_topics) and not len(b_topics):
        topics_match = True

    if not len(a_tags) and not len(b_tags):
        tags_match = True

    if topics_match and tags_match:
        write_todo(
            f"I made a nexus where I think {lobj_1['id']} and {lobj_2['id']} have same meaning, but only because both have no tags and topics. Can you check that please?")
        return True

    if not topics_match:
        if len(list(set(a_topics)&set(b_topics))):
            topics_match = True

    if not tags_match:
        if len(list(set(a_tags)&set(b_tags))):
            tags_match = True

    return topics_match and tags_match


if __name__ == '__main__':
    path = "./../output_saved/batches/adjectives_batch_1_is_groups_01_to_09.json"

    with open(f'{path}', "r") as f:
        loaded = json.load(f)
        print("Start with polish lobjs:", len(loaded))

        all_new_eng_lobjs = []
        done_pol_lobjs = []
        new_nexus_objs = []
        num = 1
        other_num = 1

        for pol_lobj in loaded:

            print("")
            print("Start", pol_lobj["id"])

            new_eng_lobjs = []

            for t in pol_lobj["translations"]["ENG"]:
                print("t = ", t)

                this_t_now_done = False

                t_without_star = t if t[0] != "*" else t[1:]

                for pell in done_pol_lobjs:
                    if t in pell["translations"]["ENG"]:

                        if is_it_the_same_meaning(pol_lobj, pell):
                            englishes = [
                                e for e in all_new_eng_lobjs
                                if e["lemma"] == t_without_star and (pol_lobj["id"] in e["»trans"] or pell["id"] in e["»trans"])
                            ]

                            for english in englishes:
                                if pol_lobj["id"] not in english["»trans"]:
                                    english["»trans"].append(pol_lobj["id"])
                                if pell["id"] not in english["»trans"]:
                                    english["»trans"].append(pell["id"])

                print("part 2")

                new_t = t

                if t[0] == "*":
                    new_t = t_without_star
                    new_t = new_t + "(þ)"
                else:
                    matching_lemma_lobjs = [en for en in all_new_eng_lobjs if en["lemma"] == t_without_star]

                    if len(matching_lemma_lobjs):
                        have_found_one_with_same_meaning = False

                        for englem in matching_lemma_lobjs:
                            trans = [xx for xx in englem["»trans"]]
                            for tran in trans:
                                plob = [el for el in loaded if el["id"] == tran][0]
                                if is_it_the_same_meaning(pol_lobj, plob):
                                    have_found_one_with_same_meaning = True
                                    this_t_now_done = True
                                    englem["»trans"].append(pol_lobj["id"])

                        if not have_found_one_with_same_meaning:
                            new_t = new_t + "(þ)"

                print("part 3")

                if this_t_now_done:
                    print("cccontinue")
                    continue

                new_id = f"eng-adj-{str(num).zfill(4)}-{new_t}"

                new_eng_lobj = {
                    "lemma": t_without_star,
                    "id": new_id,
                    "»trans": [pol_lobj["id"]],
                    # "»synonyms": [x for x in pol_lobj["translations"]["ENG"] if x != t]
                }

                print("part 4")

                new_eng_lobjs.append(new_eng_lobj)

                num = num + 1

            # new_nexus_obj = {
            #     "key": f"adj-{str(other_num).zfill(4)}-{new_eng_lobjs[0]['id'].split('-')[-1]}",
            #     "traductions": {
            #       "SPA": [],
            #       "ENG": [limmy["id"] for limmy in new_eng_lobjs],
            #       "POL": [pol_lobj["id"]]
            #     },
            #     "papers": pol_lobj["tags"],
            #     "topics": pol_lobj["topics"]
            # }
            # new_nexus_objs.append(new_nexus_obj)
            # other_num = other_num + 1

            all_new_eng_lobjs.extend(new_eng_lobjs)
            done_pol_lobjs.append(pol_lobj)

            print("Done this one.")

        f.close()

    print("Done all lobjs, so now all_new_eng_lobjs has length", len(all_new_eng_lobjs))

    all_new_eng_lobjs_json = json.dumps(all_new_eng_lobjs, indent=2, ensure_ascii=False)

    with open("../output_saved/batches/adjectives_batch_1_is_groups_01_to_09_ENG.json", "w") as outfile:
        outfile.write(all_new_eng_lobjs_json)

    # new_nexus_objs_json = json.dumps(new_nexus_objs, indent=2, ensure_ascii=False)
    # with open("./../output_saved/batches/adjectives_batch_1_is_groups_01_to_09_NEXUS.json", "w") as outfile:
    #     outfile.write(new_nexus_objs_json)

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
