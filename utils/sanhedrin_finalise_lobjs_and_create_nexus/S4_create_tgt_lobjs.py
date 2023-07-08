import json
import os
import time

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    target_lang = "ENG"
    input_override = 0  # Only set True for dryruns
    hardcoded_number_of_inputs_needed_gauged_by_dryruns = 162
    # # # # # #

    bare_input_filename = f"{wordtype}_batch_{batch}"
    input_filename = f"{bare_input_filename}_SRC"
    stem = "./../output_saved/batches/"
    input_path = f"{stem}{input_filename}"

    output_path_tgt = f"{stem}{bare_input_filename}_TGT"
    tempsave_path_tgt = output_path_tgt + "_S4_tempsave"
    # output_path_nex = f"{stem}{bare_input_filename}_NEX"
    tempsave_path_src = f"{stem}{bare_input_filename}_SRC_S4_tempsave"

    c.print_teal("input_path        =     " + c.teal(input_path))
    c.print_teal("output_path_tgt   =     " + c.teal(output_path_tgt))
    c.print_teal("tempsave_path_src =     " + c.teal(tempsave_path_src))

    all_new_tgt_lobjs = []
    done_src_lobjs = []
    # new_nexus_objs = []

    if os.path.isfile(tempsave_path_tgt + ".json"):
        with open(tempsave_path_tgt + ".json", "r") as f:
            all_new_tgt_lobjs = json.load(f)
            c.print_teal("Loaded " + str(len(all_new_tgt_lobjs)) + " items from tempsave.")
            f.close()
    else:
        c.print_teal("No tempsave_path_tgt file found, I assume you're at the start of this batch?")

    if os.path.isfile(tempsave_path_src + ".json"):
        with open(tempsave_path_src + ".json", "r") as f:
            done_src_lobjs = json.load(f)
            c.print_teal("Found tempsave file " + tempsave_path_src + " loaded " + str(len(done_src_lobjs)) + " items.")
            f.close()
    else:
        c.print_teal("No tempsave_path_src file found, I assume you're at the start of this batch?")


    def save(temp: bool = False):
        print(f"📀 {'SAVING PROGRESS' if temp else 'SAVING FINAL'}")

        _output_path_tgt = tempsave_path_tgt if temp else output_path_tgt
        _output_path_src = tempsave_path_src
        # _output_path_nex = output_path_nex + "_tempsave" if temp else output_path_nex

        # with open(_output_path_nex + ".json", "w") as outfile:
        #     new_nexus_objs_json = json.dumps(new_nexus_objs, indent=2, ensure_ascii=False)
        #     outfile.write(new_nexus_objs_json)
        #     outfile.close()

        with open(_output_path_tgt + ".json", "w") as outfile:
            all_new_tgt_lobjs_json = json.dumps(all_new_tgt_lobjs, indent=2, ensure_ascii=False)
            outfile.write(all_new_tgt_lobjs_json)
            outfile.close()

        with open(_output_path_src + ".json", "w") as outfile:
            done_src_lobjs_json = json.dumps(done_src_lobjs, indent=2, ensure_ascii=False)
            outfile.write(done_src_lobjs_json)
            outfile.close()


    with open(input_path + ".json", "r") as f:
        src_lobjs = json.load(f)
        print("Loaded", len(src_lobjs), "source lobjs.")

        how_many_inputs_needed = {"num": 0}
        matches_record = {"YES": [], "NO": []}
        tgt_lobj_id_incrementer = 1
        nexus_id_incrementer = 1

        for src_lobj_index, src_lobj in enumerate(src_lobjs):
            if src_lobj["id"] in [pl["id"] for pl in done_src_lobjs]:
                print("Skip", q(src_lobj["id"]))
                continue

            if src_lobj_index % 10 == 1:
                save(True)

            print("")
            print("")
            print("")
            print("     Starting src_lobj", q(src_lobj["id"]), f"{src_lobj_index + 1}/{len(src_lobjs)}")

            new_tgt_lobjs = []

            for tindex, t in enumerate(src_lobj["translations"][target_lang]):
                print("")
                print("")
                print("          Part 1: Check trans", c.blue(t), f'{tindex + 1}/{len(src_lobj["translations"][target_lang])}',
                      "     for", c.blue(src_lobj["id"]))

                this_t_now_done = False

                t_without_star = t if t[0] != "*" else t[1:]

                for pell in done_src_lobjs:
                    if t in pell["translations"][target_lang]:

                        is_same = is_it_the_same_meaning(src_lobj, pell, how_many_inputs_needed, matches_record,
                                                         hardcoded_number_of_inputs_needed_gauged_by_dryruns,
                                                         input_override, save, target_lang)
                        if is_same:
                            print("")
                            print("{", c.blue(src_lobj["id"]), "same as", c.blue(pell["id"]), "due to", is_same)

                            targets = [
                                e for e in all_new_tgt_lobjs
                                if e["lemma"] == t_without_star and (
                                        src_lobj["id"] in e["»trans"] or pell["id"] in e["»trans"])
                            ]

                            for target in targets:
                                if src_lobj["id"] not in target["»trans"]:
                                    print("")
                                    print("               Added1", c.blue(src_lobj["id"]), "to trans of", c.blue(target["id"]))
                                    target["»trans"].append(src_lobj["id"])
                                if pell["id"] not in target["»trans"]:
                                    print("")
                                    print("               Added1", c.blue(pell["id"]), "to trans of", c.blue(target["id"]))
                                    target["»trans"].append(pell["id"])

                print("          Part 2: Create/Merge TARGET lobj for this trans")

                new_t = t

                if t[0] == "*":
                    new_t = t_without_star
                    new_t = new_t + "(þ)"
                else:
                    matching_lemma_lobjs = [en for en in all_new_tgt_lobjs if en["lemma"] == t_without_star]

                    if len(matching_lemma_lobjs):
                        have_found_one_with_same_meaning = False

                        for targlem in matching_lemma_lobjs:
                            trans = [xx for xx in targlem["»trans"]]
                            for tran in trans:
                                slob = [el for el in src_lobjs if el["id"] == tran][0]

                                if src_lobj["id"] != slob["id"]:
                                    is_the_same = is_it_the_same_meaning(src_lobj, slob, how_many_inputs_needed,
                                                                         matches_record,
                                                                         hardcoded_number_of_inputs_needed_gauged_by_dryruns,
                                                                         input_override, save, target_lang)

                                    if is_the_same:
                                        print("")
                                        print("}", c.blue(src_lobj["id"]), "same as", c.blue(slob["id"]), "due to", is_the_same)
                                        print("")
                                        print("STOP with t", c.blue(t), "because already exist TARGET lobj", c.blue(targlem["id"]),
                                              targlem["»trans"])

                                        have_found_one_with_same_meaning = True
                                        this_t_now_done = True

                                        if src_lobj["id"] not in targlem["»trans"]:
                                            print("")
                                            print("               Added2", c.blue(src_lobj["id"]), "to trans of",
                                                  c.blue(targlem["id"]))
                                            targlem["»trans"].append(src_lobj["id"])

                        if not have_found_one_with_same_meaning:
                            new_t = new_t + "(þ)"

                if this_t_now_done:
                    print("Stop")
                    continue

                new_id = f"{target_lang.lower()}-{wordtype}-{str(tgt_lobj_id_incrementer).zfill(4)}-{new_t}"

                print("")
                print(f"          Part 3: Create NEW target ({target_lang}) lobj", q(new_id))

                new_tgt_lobj = {
                    "lemma": t_without_star,
                    "id": new_id,
                    "»trans": [src_lobj["id"]],
                    # "»synonyms": [x for x in src_lobj["translations"][target_lang] if x != t]
                }

                new_tgt_lobjs.append(new_tgt_lobj)

                tgt_lobj_id_incrementer = tgt_lobj_id_incrementer + 1

            # new_nexus_obj = {
            #     "key": f"{wordtype}-{str(nexus_id_incrementer).zfill(4)}-{new_tgt_lobjs[0]['id'].split('-')[-1]}",
            #     "traductions": {
            #       "SPA": [],
            #       target_lang: [limmy["id"] for limmy in new_tgt_lobjs],
            #       "POL": [src_lobj["id"]]
            #     },
            #     "papers": src_lobj["tags"],
            #     "topics": src_lobj["topics"]
            # }
            # new_nexus_objs.append(new_nexus_obj)
            # nexus_id_incrementer = nexus_id_incrementer + 1

            all_new_tgt_lobjs.extend(new_tgt_lobjs)
            done_src_lobjs.append(src_lobj)

            print("")
            print("     Done this one.")

        f.close()

    print("")
    print("Done all lobjs, so now all_new_tgt_lobjs has length", len(all_new_tgt_lobjs))
    print("how_many_inputs_needed", how_many_inputs_needed)

    print("Completely done.")

    for l in all_new_tgt_lobjs:
        if l["lemma"][0] == "*":
            l["lemma"] = l["lemma"][1:]

    save()
