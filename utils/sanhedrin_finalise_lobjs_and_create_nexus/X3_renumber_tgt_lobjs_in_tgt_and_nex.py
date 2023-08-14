from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c, load_data, save

if __name__ == '__main__':

    # # # # # #
    wordtype = "ver"
    batch = "01"
    id_start_number = 1
    reorder_so_siblings_consequent = False
    # # # # # #

    tgt_input_filename = f"{wordtype}_batch_{batch}_TGT"
    nex_input_filename = f"{wordtype}_batch_{batch}_NEX"

    stem = "./../../output_saved/batches/"

    tgt_input_path = f"{stem}{tgt_input_filename}"
    nex_input_path = f"{stem}{nex_input_filename}"

    c.print_teal("tgt_input_path    =     " + c.teal(tgt_input_path))
    c.print_teal("nex_input_path    =     " + c.teal(nex_input_path))
    c.print_teal("No tempsave file is used in this stage..")

    tgt = load_data(tgt_input_path)
    c.print_yellow("Loaded " + tgt_input_path)
    nex = load_data(nex_input_path)
    c.print_yellow("Loaded " + nex_input_path)

    if reorder_so_siblings_consequent:
        tgt_new = {}
        for tarlob in tgt:
            if tarlob["lemma"] in tgt_new:
                tgt_new[tarlob["lemma"]].append(tarlob)
            else:
                tgt_new[tarlob["lemma"]] = [tarlob]
        tgt_new_arr = []
        for tarkey in tgt_new:
            for tarlob in tgt_new[tarkey]:
                tgt_new_arr.append(tarlob)
        tgt = tgt_new_arr

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

    save(tgt_input_path, None, tgt)
    save(nex_input_path, None, nex)

    print("Completely done.")
