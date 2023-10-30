from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword, run_sanhedrin
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import Color as c, load_data, save

if __name__ == '__main__':

    # # # # # #
    wordtypes = []  # Leave blank for all.
    batch = "01"
    id_start_num = 1
    # # # # # #

    def go(wordtype):
        id_start_number = id_start_num
        nex_input_filename = f"{wordtype}_batch_{batch}_NEX"

        stem = "./../../output_saved/batches/done/"

        nex_input_path = f"{stem}{nex_input_filename}"

        c.print_teal("nex_input_path    =     " + c.teal(nex_input_path))
        c.print_teal("No tempsave file is used in this stage..")

        nex = load_data(nex_input_path)
        c.print_yellow("Loaded " + nex_input_path)

        print("Loaded", len(nex), "nexus objs.")

        for nobj in nex:
            new_id_number = "0000" + str(id_start_number)
            new_id_number = new_id_number[-4:]
            id_start_number += 1

            old_id = nobj["key"]
            split = old_id.split("-")
            split[1] = str(new_id_number)
            new_id = "-".join(split)

            nobj["key"] = new_id

        save(nex_input_path, None, nex)

        print("Completely done.")


    run_sanhedrin(go, wordtypes)
