import json
import os
import time

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing


#
#
# This main.py is just for checking lemma objects.
#
#

def q(s):
    return f'"{s}"'


def is_it_the_same_meaning(lobj_1, lobj_2, input_counter, matches_record, total_anticipated):
    input_override = 0  # Should be 0, set as True only for testing purposes.

    for match_record in matches_record["YES"]:
        if len(match_record) == 2 and lobj_1["id"] in match_record and lobj_2["id"] in match_record:
            return "ALREADY CONFIRMED"
    for match_record in matches_record["NO"]:
        if len(match_record) == 2 and lobj_1["id"] in match_record and lobj_2["id"] in match_record:
            return False

    def record_it(bool):
        matches_record["YES" if bool else "NO"].append([lobj_1["id"], lobj_2["id"]])

    a_topics = lobj_1["topics"]
    b_topics = lobj_2["topics"]
    a_tags = [y for y in lobj_1["tags"] if y[:4] != "FREQ"]
    b_tags = [y for y in lobj_2["tags"] if y[:4] != "FREQ"]

    if "extra" in lobj_2:
        if "synonyms" in lobj_2["extra"]:
            if lobj_1["lemma"] in lobj_2["extra"]["synonyms"]:
                record_it(True)
                return "LISTED SYNONYM"

    if "extra" in lobj_1:
        if "synonyms" in lobj_1["extra"]:
            if lobj_2["lemma"] in lobj_1["extra"]["synonyms"]:
                record_it(True)
                return "LISTED SYNONYM"

    topics_match = False
    tags_match = False

    if not len(a_topics) and not len(b_topics):
        topics_match = True

    if not len(a_tags) and not len(b_tags):
        tags_match = True

    if topics_match and tags_match:
        write_todo(
            f"I made a nexus where I think {lobj_1['id']} and {lobj_2['id']} have same meaning, but only because both have no tags and topics. Can you check that please?")
        record_it(True)
        return "NO TAGS OR TOPICS"

    if not topics_match:
        if len(list(set(a_topics) & set(b_topics))):
            topics_match = True

    if not tags_match:
        if len(list(set(a_tags) & set(b_tags))):
            tags_match = True

    if topics_match and tags_match:
        print("")
        print("**********************************")
        print("")
        print(lobj_1["id"], "", lobj_1["translations"]["ENG"])
        print(a_tags)
        print(a_topics)
        print("")
        print(lobj_2["id"], "", lobj_2["translations"]["ENG"])
        print(b_tags)
        print(b_topics)
        print("")
        print("**********************************")
        print("")

        input_counter["num"] += 1

        confirmation = True
        interval = 0

        if not input_override:
            confirmation = input(f"{input_counter['num']}/{total_anticipated} same?\n")
            interval = 0.33

        if confirmation:
            print("")
            print("💚💚")
            print("💚💚")
            record_it(True)
            time.sleep(interval)
            return "TAGS AND TOPICS MATCH"
        else:
            print("")
            print(" 🟥")
            print("")
            time.sleep(interval)

    record_it(False)


if __name__ == '__main__':
    path = "./../output_saved/batches/adjectives_batch_1_is_groups_01_to_09.json"

    with open(f'{path}', "r") as f:
        pol_lobjs = json.load(f)
        print("Loaded", len(pol_lobjs), "polish lobjs.")

        all_new_eng_lobjs = []
        done_pol_lobjs = []
        new_nexus_objs = []

        how_many_inputs_needed = {"num": 0}
        hardcoded_number_of_inputs_needed_gauged_by_dryruns = 162
        matches_record = {"YES": [], "NO": []}
        num = 1
        other_num = 1

        for pol_lobj_index, pol_lobj in enumerate(pol_lobjs):

            print("")
            print("")
            print("")
            print("     Starting pol_lobj", q(pol_lobj["id"]), f"{pol_lobj_index + 1}/{len(pol_lobjs)}")

            new_eng_lobjs = []

            for tindex, t in enumerate(pol_lobj["translations"]["ENG"]):
                print("")
                print("")
                print("          Part 1: Check trans", q(t), f'{tindex + 1}/{len(pol_lobj["translations"]["ENG"])}',
                      "     for", q(pol_lobj["id"]))

                this_t_now_done = False

                t_without_star = t if t[0] != "*" else t[1:]

                for pell in done_pol_lobjs:
                    if t in pell["translations"]["ENG"]:

                        is_same = is_it_the_same_meaning(pol_lobj, pell, how_many_inputs_needed, matches_record, hardcoded_number_of_inputs_needed_gauged_by_dryruns)
                        if is_same:
                            print("")
                            print("{", q(pol_lobj["id"]), "same as", q(pell["id"]), "due to", is_same)

                            englishes = [
                                e for e in all_new_eng_lobjs
                                if e["lemma"] == t_without_star and (
                                        pol_lobj["id"] in e["»trans"] or pell["id"] in e["»trans"])
                            ]

                            for english in englishes:
                                if pol_lobj["id"] not in english["»trans"]:
                                    # print("$1", f'["{pol_lobj["id"]}","{pell["id"]}"]')  # Same meaning - check this.
                                    print("")
                                    print("               Added1", q(pol_lobj["id"]), "to trans of", q(english["id"]))
                                    english["»trans"].append(pol_lobj["id"])
                                if pell["id"] not in english["»trans"]:
                                    # print("$1", f'["{pol_lobj["id"]}","{pell["id"]}"]')  # Same meaning - check this.
                                    print("")
                                    print("               Added1", q(pell["id"]), "to trans of", q(english["id"]))
                                    english["»trans"].append(pell["id"])

                print("          Part 2: Create/Merge ENG lobj for this trans")

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
                                plob = [el for el in pol_lobjs if el["id"] == tran][0]

                                if pol_lobj["id"] != plob["id"]:
                                    is_the_same = is_it_the_same_meaning(pol_lobj, plob, how_many_inputs_needed, matches_record, hardcoded_number_of_inputs_needed_gauged_by_dryruns)

                                    if is_the_same:
                                        print("")
                                        print("}", q(pol_lobj["id"]), "same as", q(plob["id"]), "due to", is_the_same)
                                        print("")
                                        print("STOP with t", q(t), "because already exist ENG lobj", q(englem["id"]),
                                              englem["»trans"])

                                        have_found_one_with_same_meaning = True
                                        this_t_now_done = True

                                        if pol_lobj["id"] not in englem["»trans"]:
                                            # print("$2",f'["{pol_lobj["id"]}","{plob["id"]}"]')  # Same meaning - check this.
                                            print("")
                                            print("               Added2", q(pol_lobj["id"]), "to trans of",
                                                  q(englem["id"]))
                                            englem["»trans"].append(pol_lobj["id"])

                        if not have_found_one_with_same_meaning:
                            new_t = new_t + "(þ)"

                if this_t_now_done:
                    print("stop")
                    continue

                new_id = f"eng-adj-{str(num).zfill(4)}-{new_t}"

                print("")
                print("          Part 3: Create NEW eng lobj", q(new_id))

                new_eng_lobj = {
                    "lemma": t_without_star,
                    "id": new_id,
                    "»trans": [pol_lobj["id"]],
                    # "»synonyms": [x for x in pol_lobj["translations"]["ENG"] if x != t]
                }

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

            print("")
            print("     Done this one.")

        f.close()

    print("")
    print("Done all lobjs, so now all_new_eng_lobjs has length", len(all_new_eng_lobjs))
    print("how_many_inputs_needed", how_many_inputs_needed)

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
