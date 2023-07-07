import json
import os
import time

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.generate_eng_from_pol.tools import is_it_the_same_meaning, q
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    input_override = 0  # Only set True for dryruns
    hardcoded_number_of_inputs_needed_gauged_by_dryruns = 162
    # # # # # #

    bare_input_filename = f"{wordtype}_batch_{batch}"
    input_filename = f"{bare_input_filename}_SAN"
    stem = "./../output_saved/batches/"
    input_path = f"{stem}{input_filename}"

    output_path_eng = f"{stem}{bare_input_filename}_ENG"
    tempsave_path_eng = output_path_eng + "_S4_tempsave"
    # output_path_nex = f"{stem}{bare_input_filename}_NEX"
    tempsave_path_pol = f"{stem}{bare_input_filename}_POL_S4_tempsave"

    c.print_teal("input_path        =     " + c.teal(input_path))
    c.print_teal("output_path_eng   =     " + c.teal(output_path_eng))
    c.print_teal("tempsave_path_pol =     " + c.teal(tempsave_path_pol))

    all_new_eng_lobjs = []
    done_pol_lobjs = []
    # new_nexus_objs = []

    if os.path.isfile(tempsave_path_eng + ".json"):
        with open(tempsave_path_eng + ".json", "r") as f:
            all_new_eng_lobjs = json.load(f)
            c.print_teal("Loaded " + str(len(all_new_eng_lobjs)) + " items from tempsave.")
            f.close()
    else:
        c.print_teal("No tempsave_path_eng file found, I assume you're at the start of this batch?")

    if os.path.isfile(tempsave_path_pol + ".json"):
        with open(tempsave_path_pol + ".json", "r") as f:
            done_pol_lobjs = json.load(f)
            c.print_teal("Found tempsave file " + tempsave_path_pol + " loaded " + str(len(done_pol_lobjs)) + " items.")
            f.close()
    else:
        c.print_teal("No tempsave_path_pol file found, I assume you're at the start of this batch?")


    def save(temp: bool = False):
        print(f"📀 {'SAVING PROGRESS' if temp else 'SAVING FINAL'}")

        _output_path_eng = tempsave_path_eng if temp else output_path_eng
        _output_path_pol = tempsave_path_pol
        # _output_path_nex = output_path_nex + "_tempsave" if temp else output_path_nex

        # with open(_output_path_nex + ".json", "w") as outfile:
        #     new_nexus_objs_json = json.dumps(new_nexus_objs, indent=2, ensure_ascii=False)
        #     outfile.write(new_nexus_objs_json)
        #     outfile.close()

        with open(_output_path_eng + ".json", "w") as outfile:
            all_new_eng_lobjs_json = json.dumps(all_new_eng_lobjs, indent=2, ensure_ascii=False)
            outfile.write(all_new_eng_lobjs_json)
            outfile.close()

        with open(_output_path_pol + ".json", "w") as outfile:
            done_pol_lobjs_json = json.dumps(done_pol_lobjs, indent=2, ensure_ascii=False)
            outfile.write(done_pol_lobjs_json)
            outfile.close()


    with open(input_path + ".json", "r") as f:
        pol_lobjs = json.load(f)
        print("Loaded", len(pol_lobjs), "polish lobjs.")

        how_many_inputs_needed = {"num": 0}
        matches_record = {"YES": [], "NO": []}
        eng_lobj_id_incrementer = 1
        nexus_id_incrementer = 1

        for pol_lobj_index, pol_lobj in enumerate(pol_lobjs):
            if pol_lobj["id"] in [pl["id"] for pl in done_pol_lobjs]:
                print("skip", q(pol_lobj["id"]))
                continue

            if pol_lobj_index % 10 == 1:
                save(True)

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

                        is_same = is_it_the_same_meaning(pol_lobj, pell, how_many_inputs_needed, matches_record,
                                                         hardcoded_number_of_inputs_needed_gauged_by_dryruns,
                                                         input_override, save)
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
                                    print("")
                                    print("               Added1", q(pol_lobj["id"]), "to trans of", q(english["id"]))
                                    english["»trans"].append(pol_lobj["id"])
                                if pell["id"] not in english["»trans"]:
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
                                    is_the_same = is_it_the_same_meaning(pol_lobj, plob, how_many_inputs_needed,
                                                                         matches_record,
                                                                         hardcoded_number_of_inputs_needed_gauged_by_dryruns,
                                                                         input_override, save)

                                    if is_the_same:
                                        print("")
                                        print("}", q(pol_lobj["id"]), "same as", q(plob["id"]), "due to", is_the_same)
                                        print("")
                                        print("STOP with t", q(t), "because already exist ENG lobj", q(englem["id"]),
                                              englem["»trans"])

                                        have_found_one_with_same_meaning = True
                                        this_t_now_done = True

                                        if pol_lobj["id"] not in englem["»trans"]:
                                            print("")
                                            print("               Added2", q(pol_lobj["id"]), "to trans of",
                                                  q(englem["id"]))
                                            englem["»trans"].append(pol_lobj["id"])

                        if not have_found_one_with_same_meaning:
                            new_t = new_t + "(þ)"

                if this_t_now_done:
                    print("stop")
                    continue

                new_id = f"eng-{wordtype}-{str(eng_lobj_id_incrementer).zfill(4)}-{new_t}"

                print("")
                print("          Part 3: Create NEW eng lobj", q(new_id))

                new_eng_lobj = {
                    "lemma": t_without_star,
                    "id": new_id,
                    "»trans": [pol_lobj["id"]],
                    # "»synonyms": [x for x in pol_lobj["translations"]["ENG"] if x != t]
                }

                new_eng_lobjs.append(new_eng_lobj)

                eng_lobj_id_incrementer = eng_lobj_id_incrementer + 1

            # new_nexus_obj = {
            #     "key": f"{wordtype}-{str(nexus_id_incrementer).zfill(4)}-{new_eng_lobjs[0]['id'].split('-')[-1]}",
            #     "traductions": {
            #       "SPA": [],
            #       "ENG": [limmy["id"] for limmy in new_eng_lobjs],
            #       "POL": [pol_lobj["id"]]
            #     },
            #     "papers": pol_lobj["tags"],
            #     "topics": pol_lobj["topics"]
            # }
            # new_nexus_objs.append(new_nexus_obj)
            # nexus_id_incrementer = nexus_id_incrementer + 1

            all_new_eng_lobjs.extend(new_eng_lobjs)
            done_pol_lobjs.append(pol_lobj)

            print("")
            print("     Done this one.")

        f.close()

    print("")
    print("Done all lobjs, so now all_new_eng_lobjs has length", len(all_new_eng_lobjs))
    print("how_many_inputs_needed", how_many_inputs_needed)

    print("Completely done.")

    for l in all_new_eng_lobjs:
        if l["lemma"][0] == "*":
            l["lemma"] = l["lemma"][1:]

    save()
