from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword, run_sanhedrin, get_unused, get_nonexisting
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c, load_data, save

if __name__ == '__main__':

    # # # # # #
    wordtypes = []  # Leave blank for all.
    batch = "01"
    tgt_lang = "ENG"
    src_lang = "POL"
    # # # # # #

    def go(wordtype):
        tgt_input_filename = f"{wordtype}_batch_{batch}_TGT"
        src_input_filename = f"{wordtype}_batch_{batch}_SRC"
        nex_input_filename = f"{wordtype}_batch_{batch}_NEX"

        stem = "./../../output_saved/batches/done/"

        tgt_input_path = f"{stem}{tgt_input_filename}"
        src_input_path = f"{stem}{src_input_filename}"
        nex_input_path = f"{stem}{nex_input_filename}"

        c.print_teal("tgt_input_path    =     " + c.teal(tgt_input_path))
        c.print_teal("src_input_path    =     " + c.teal(src_input_path))
        c.print_teal("nex_input_path    =     " + c.teal(nex_input_path))
        c.print_teal("No tempsave file is used in this stage..")

        tgt = load_data(tgt_input_path)
        c.print_yellow("Loaded " + tgt_input_path)
        src = load_data(src_input_path)
        c.print_yellow("Loaded " + src_input_path)
        nex = load_data(nex_input_path)
        c.print_yellow("Loaded " + nex_input_path)

        print("Loaded", len(tgt), "target lobjs.")
        print("Loaded", len(src), "source lobjs.")
        print("Loaded", len(nex), "nexus objs.")

        res = {}

        res["unused_tgt"] = get_unused(tgt, nex, tgt_lang)
        res["unused_src"] = get_unused(src, nex, src_lang)

        res["nonexisting_tgt"] = get_nonexisting(tgt, nex, tgt_lang)
        res["nonexisting_src"] = get_nonexisting(src, nex, src_lang)

        print("")
        for key in res:
            c.print_blue(f"{len(res[key])} {key}")

        print("")
        for key in res:
            if len(res[key]):
                c.print_red(key + ":")
                for item in res[key]:
                    print(item)

        print("\nCompletely done.")


    run_sanhedrin(go, wordtypes)
