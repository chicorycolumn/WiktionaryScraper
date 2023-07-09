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
    nexus_id_start_number = 1
    # # # # # #

    src_input_filename = f"{wordtype}_batch_{batch}_SRC"
    tgt_input_filename = f"{wordtype}_batch_{batch}_TGT"
    output_filename = f"{wordtype}_batch_{batch}_NEX"

    stem = "./../../output_saved/batches/"

    src_input_path = f"{stem}{src_input_filename}"
    tgt_input_path = f"{stem}{tgt_input_filename}"
    output_path = f"{stem}{output_filename}"

    # tempsave_path = input_path + "_S5_tempsave"

    c.print_teal("src_input_path    =     " + c.teal(src_input_path))
    c.print_teal("tgt_input_path    =     " + c.teal(tgt_input_path))
    c.print_teal("output_path    =     " + c.teal(output_path))
    c.print_teal("No tempsave file is used in this stage..")

    def save(data):
        print(f"📀 {'SAVING FINAL'}")

        _output_path = output_path

        with open(_output_path + ".json", "w") as outfile:
            print(f'Writing {len(data)} results.')
            data_json = json.dumps(data, indent=2, ensure_ascii=False)
            outfile.write(data_json)
            outfile.close()

    src = []
    tgt = []
    nex = []

    with open(src_input_path + ".json", "r") as f:
        src = json.load(f)
        f.close()
    with open(tgt_input_path + ".json", "r") as f:
        tgt = json.load(f)
        f.close()

    print("Loaded", len(src), "source lobjs.")
    print("Loaded", len(tgt), "target lobjs.")

    records = []

    for src_lobj in src:
        already_done = False

        for r in records:
            if not already_done and src_lobj["id"] in r["src"]:
                already_done = True

        if already_done:
            continue

        tgt_connections = []
        for tgt_lobj in tgt:
            print(tgt_lobj)
            if src_lobj["id"] in tgt_lobj["»trans"]:
                tgt_connections.append(tgt_lobj)

        src_connections = []

        for tgt_connection in tgt_connections:
            src_connections.extend(tgt_connection["»trans"])

        src_list = list(set(src_connections))
        tgt_list = list(set([tarl["id"] for tarl in tgt_connections]))

        if len(src_list) == 0 or len(tgt_list) == 0:
            c.print_red("Empty records for:")
            print(src_lobj)
            print("src_list", src_list)
            print("tgt_list", tgt_list)
            raise Exception("Stop")

        records.append({
            "src": src_list,
            "tgt": tgt_list
        })

    nexus_objects = []
    empty_records = []

    for record_index, record in enumerate(records):
        if len(record["src"]) == 0 or len(record["tgt"]) == 0:
            empty_records.append(record)
    if len(empty_records):
        c.print_red("Empty records:")
        for empty_record in empty_records:
            print(empty_record)
        raise Exception("Stop")

    for record_index, record in enumerate(records):
        new_id_number = "0000" + str(nexus_id_start_number)
        new_id_number = new_id_number[-4:]
        nexus_id_start_number += 1

        print(11, record['tgt'])
        new_nexus_id = f"{wordtype}-{new_id_number}-{record['tgt'][0].split('-')[-1]}"

        new_nexus_obj = {
            "key": new_nexus_id,
            "traductions": {
              "SPA": [],
              "ENG": record["tgt"],
              "POL": record["src"]
            },
            "papers": src_lobj["tags"],
            "topics": src_lobj["topics"]
        }
        nex.append(new_nexus_obj)

    print("")
    print("Completely done.")

    save(nex)
