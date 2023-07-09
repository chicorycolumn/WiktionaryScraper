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

    src_input_filename = f"{wordtype}_batch_{batch}_SRC"
    tgt_input_filename = f"{wordtype}_batch_{batch}_TGT"

    stem = "./../../output_saved/batches/"

    src_input_path = f"{stem}{src_input_filename}"
    tgt_input_path = f"{stem}{tgt_input_filename}"

    # tempsave_path = input_path + "_S5_tempsave"

    c.print_teal("src_input_path    =     " + c.teal(src_input_path))
    c.print_teal("tgt_input_path    =     " + c.teal(tgt_input_path))
    c.print_teal("No tempsave file is used in this stage..")

    src = []
    tgt = []

    with open(src_input_path + ".json", "r") as f:
        src = json.load(f)
        f.close()
    with open(tgt_input_path + ".json", "r") as f:
        tgt = json.load(f)
        f.close()

    print("Loaded", len(src), "source lobjs.")
    print("Loaded", len(tgt), "target lobjs.")

    for slob in src:
        new_id_number = "0000" + str(id_start_number)
        new_id_number = new_id_number[-4:]
        id_start_number += 1

        old_id = slob["id"]
        split = old_id.split("-")
        split[2] = str(new_id_number)
        new_id = "-".join(split)

        slob["id"] = new_id

        for tlob in tgt:
            if old_id in tlob["»trans"]:
                new_trans = []
                for tran in tlob["»trans"]:
                    if tran == old_id:
                        new_trans.append(new_id)
                    else:
                        new_trans.append(tran)
                tlob["»trans"] = new_trans

    with open(src_input_path + ".json", "w") as outfile:
        print(f'Writing {len(src)} src results.')
        data_json = json.dumps(src, indent=2, ensure_ascii=False)
        outfile.write(data_json)
        outfile.close()
        
    with open(tgt_input_path + ".json", "w") as outfile:
        print(f'Writing {len(tgt)} tgt results.')
        data_json = json.dumps(tgt, indent=2, ensure_ascii=False)
        outfile.write(data_json)
        outfile.close()