import json
import os
import time

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.generate_eng_from_pol.tools import is_it_the_same_meaning, q, add_hints, get_signalword, test_signalword
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    # # # # # #

    input_filename = f"{wordtype}_batch_{batch}_ENG"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"
    tempsave_path = input_path + "_S5_tempsave"

    c.print_teal("input_path    =     " + c.teal(input_path))
    c.print_teal("tempsave_path =     " + c.teal(tempsave_path))
    c.print_teal("Output path will be the same as input.")


    def save(eng_lobjs, temp: bool = False):
        print(f"📀 {'SAVING PROGRESS' if temp else 'SAVING FINAL'}")

        _input_path = tempsave_path if temp else input_path

        with open(_input_path + ".json", "w") as outfile:
            res_json = json.dumps(eng_lobjs, indent=2, ensure_ascii=False)
            outfile.write(res_json)
            outfile.close()

    eng_lobjs = []
    siblings = []
    sibling_headers = []

    if os.path.isfile(tempsave_path + ".json"):
        with open(tempsave_path + ".json", "r") as f:
            eng_lobjs = json.load(f)
            c.print_teal("Loaded " + str(len(eng_lobjs)) + " items from tempsave.")
            f.close()
    else:
        c.print_teal("No tempsave_path file found, I assume you're at the start of this batch?")
        with open(input_path + ".json", "r") as f:
            eng_lobjs = json.load(f)
            f.close()

    print("Loaded", len(eng_lobjs), "english lobjs.")

    for index_1, eng_lobj_1 in enumerate(eng_lobjs):
        if eng_lobj_1["lemma"] not in sibling_headers:
            sibling_set = [eng_lobj_1]
            for index_2, eng_lobj_2 in enumerate(eng_lobjs):
                if index_1 != index_2 and eng_lobj_1["lemma"] == eng_lobj_2["lemma"]:
                    sibling_set.append(eng_lobj_2)
            if len(sibling_set) > 1:
                siblings.append(sibling_set)
                sibling_headers.append(eng_lobj_1["lemma"])

    print(f"There are {len(siblings)} sibling sets.")
    for sib_set in siblings:
        print(sib_set)

    print(f"There are {len(siblings)} sibling sets.")
    for sib_set_index, sib_set in enumerate(siblings):
        signalwords = [get_signalword(l["id"]) for l in sib_set]
        failed = False
        for signalword in signalwords:
            if not test_signalword(signalword):
                failed = True

        print("")
        print(f"{sib_set_index + 1}/{len(siblings)}")

        if not failed:
            c.print_green("ALREADY LOOKS DONE")
            for sibl in sib_set:
                c.print_green(get_signalword(sibl["id"]))
                print(sibl)
            continue

        if sib_set_index % 10 == 1:
            save(eng_lobjs, True)

        add_hints(sib_set)

    print("")
    print("Completely done.")

    save(eng_lobjs)
