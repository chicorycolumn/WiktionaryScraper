import json
import os
import time

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, get_signalword, test_signalword
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    id_start_number = 1
    # # # # # #

    tgt_input_filename = f"{wordtype}_batch_{batch}_TGT"
    nex_input_filename = f"{wordtype}_batch_{batch}_NEX"

    stem = "./../../output_saved/batches/"

    tgt_input_path = f"{stem}{tgt_input_filename}"
    nex_input_path = f"{stem}{nex_input_filename}"

    c.print_teal("tgt_input_path    =     " + c.teal(tgt_input_path))
    c.print_teal("nex_input_path    =     " + c.teal(nex_input_path))
    c.print_teal("No tempsave file is used in this stage..")

    tgt = []
    nex = []

    with open(tgt_input_path + ".json", "r") as f:
        tgt = json.load(f)
        f.close()
    with open(nex_input_path + ".json", "r") as f:
        nex = json.load(f)
        f.close()

    print("Loaded", len(tgt), "source lobjs.")
    print("Loaded", len(nex), "nexus objs.")

    for slob in tgt:
        new_id_number = "0000" + str(id_start_number)
        new_id_number = new_id_number[-4:]
        id_start_number += 1

        old_id = slob["id"]
        split = old_id.split("-")
        split[2] = str(new_id_number)
        new_id = "-".join(split)

        slob["id"] = new_id

        for nlob in nex:
            for key in nlob["traductions"]:
                if old_id in nlob["traductions"][key]:
                    new_trans = []
                    for tran in nlob["traductions"][key]:
                        if tran == old_id:
                            new_trans.append(new_id)
                        else:
                            new_trans.append(tran)
                    nlob["traductions"][key] = new_trans

    with open(tgt_input_path + ".json", "w") as outfile:
        print(f'Writing {len(tgt)} tgt results.')
        data_json = json.dumps(tgt, indent=2, ensure_ascii=False)
        outfile.write(data_json)
        outfile.close()
        
    with open(nex_input_path + ".json", "w") as outfile:
        print(f'Writing {len(nex)} nexus results.')
        data_json = json.dumps(nex, indent=2, ensure_ascii=False)
        outfile.write(data_json)
        outfile.close()