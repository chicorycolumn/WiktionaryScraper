from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword, run_sanhedrin, renumber_inflections_root
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import Color as c, load_data, save

if __name__ == '__main__':

    # # # # # #
    wordtypes = []  # Leave blank for all.
    batch = "01"
    stage = 2  # Stage 1 is manual resolution for problematics only, Stage 2 is automatic of all.
    # # # # # #

    def go(wordtype):
        tgt_input_filename = f"{wordtype}_batch_{batch}_TGT"
        src_input_filename = f"{wordtype}_batch_{batch}_SRC"

        stem = "./../../output_saved/batches/done/"
        src_input_path = f"{stem}{src_input_filename}"
        tgt_input_path = f"{stem}{tgt_input_filename}"
        c.print_teal("No tempsave file is used in this stage..")

        c.print_teal("tgt_input_path    =     " + c.teal(tgt_input_path))
        src = load_data(src_input_path)
        c.print_yellow("Loaded " + src_input_path)
        renumber_inflections_root(stage, src, save, src_input_path)

        c.print_teal("src_input_path    =     " + c.teal(src_input_path))
        tgt = load_data(tgt_input_path)
        c.print_yellow("Loaded " + tgt_input_path)
        renumber_inflections_root(stage, tgt, save, tgt_input_path)


        print("Completely done.")


    run_sanhedrin(go, wordtypes)
