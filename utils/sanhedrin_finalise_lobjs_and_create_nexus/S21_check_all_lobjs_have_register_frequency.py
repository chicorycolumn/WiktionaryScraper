from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_allohom_info, \
    run_sanhedrin_with_suffixes
from utils.postprocessing.common import finalise_lemma_objects, add_tags_and_topics_from_shorthand
from utils.scraping.Polish_dicts import shorthand_tag_refs
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import Color as c, get_curried_save, load_data

if __name__ == '__main__':

    # # # # # #
    wordtypes = []  # Leave blank for all.
    batch = "01"
    suffixes = []  # Leave blank for both SRC and TGT.
    run_this_part_only = 0  # 0 for both, otherwise 1 or 2.

    # # # # # #


    def go(wordtype, suffix):
        input_filename = f"{wordtype}_batch_{batch}_{suffix}"
        stem = "./../../output_saved/batches/done/"
        input_path = f"{stem}{input_filename}"
        save = get_curried_save(input_path, None)

        c.print_teal("input_path =     " + c.teal(input_path))
        c.print_teal("Output path will be the same as input.")
        c.print_teal("No tempsave files are used for this stage.")

        lobjs = load_data(input_path)

        keys_to_check_exist_on_all = ["register", "frequency"]

        for lobj in lobjs:
            for key_to_check_exist_on_all in keys_to_check_exist_on_all:
                if key_to_check_exist_on_all not in lobj:
                    print("🚩", lobj["id"])
                    lobj[key_to_check_exist_on_all] = '🚩'

        save(lobjs)

        print("Completely done.")

    run_sanhedrin_with_suffixes(go, wordtypes, suffixes)
