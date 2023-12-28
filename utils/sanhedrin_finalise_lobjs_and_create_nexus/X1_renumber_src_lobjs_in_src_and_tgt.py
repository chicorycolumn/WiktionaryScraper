from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword, run_sanhedrin
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import Color as c, load_data, save

if __name__ == '__main__':

    # # # # # #
    wordtypes = ["adj"]  # Leave blank for all.
    batch = "01"
    id_start_number = 1
    # # # # # #

    def go(wordtype, id_start_number):
        src_input_filename = f"{wordtype}_batch_{batch}_SRC"
        tgt_input_filename = f"{wordtype}_batch_{batch}_TGT"

        stem = "./../../output_saved/batches/"

        src_input_path = f"{stem}{src_input_filename}"
        tgt_input_path = f"{stem}{tgt_input_filename}"

        # tempsave_path = input_path + "_S5_tempsave"

        c.print_teal("src_input_path    =     " + c.teal(src_input_path))
        c.print_teal("tgt_input_path    =     " + c.teal(tgt_input_path))
        c.print_teal("No tempsave file is used in this stage..")

        src = load_data(src_input_path)
        tgt = load_data(tgt_input_path)

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

        save(src_input_path, None, src)
        save(tgt_input_path, None, tgt)

        print("Completely done.")

    run_sanhedrin(go, wordtypes, [id_start_number])