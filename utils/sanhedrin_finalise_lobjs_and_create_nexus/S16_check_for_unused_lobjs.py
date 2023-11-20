from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword, run_sanhedrin, get_unused, get_nonexisting
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import Color as c, load_data, save

if __name__ == '__main__':

    # # # # # #
    wordtypes = []  # Leave blank for all.
    batch = "01"
    tgt_lang = "ENG"
    src_lang = "POL"
    # # # # # #

    def add_to_res_dict(main_dict_key, wordtype, res_dict, results_list):
        main_res_dict = []
        ignored_res_dict = []
        for result_str in results_list:
            if result_str.split("-")[1] == wordtype:
                main_res_dict.append(result_str)
            else:
                ignored_res_dict.append(result_str)
        res_dict[main_dict_key] = main_res_dict
        res_dict[main_dict_key + "_IGNORED"] = ignored_res_dict

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

        add_to_res_dict("unused_tgt", wordtype, res, get_unused(tgt, nex, tgt_lang))
        add_to_res_dict("unused_src", wordtype, res, get_unused(src, nex, src_lang))
        add_to_res_dict("nonexisting_tgt", wordtype, res, get_nonexisting(tgt, nex, tgt_lang))
        add_to_res_dict("nonexisting_src", wordtype, res, get_nonexisting(src, nex, src_lang))

        non_ignored_keys = []
        ignored_keys = []
        for k in res:
            if k.endswith("_IGNORED"):
                ignored_keys.append(k)
            else:
                non_ignored_keys.append(k)

        print("")
        for key in non_ignored_keys:
            c.print_blue(f"{len(res[key])} {key}")

        if all(len(res[key]) == 0 for key in non_ignored_keys):
            print("🟢 All resolved.")

        print("")
        for key in non_ignored_keys:
            if len(res[key]):
                c.print_red(key + ":")
                for item in res[key]:
                    print(f'"{item}"')

        print("")
        for key in ignored_keys:
            if len(res[key]):
                c.print_yellow(key + ":")
                for item in res[key]:
                    print(f'"{item}"')

        print("\nCompletely done.")

    run_sanhedrin(go, wordtypes)
