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
    just_list_them = True  # Should be False
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

        to_do_lobjs = []
        for lobj in lobjs:
            if "(" in lobj["id"]:
                if "allohomInfo" not in lobj or not lobj["allohomInfo"]:
                    to_do_lobjs.append(lobj)

        c.print_bold(f"{len(to_do_lobjs)} need allohomInfo added.")
        if just_list_them:
            for l in to_do_lobjs:
                print(l['id'])
            print('')
        else:
            cmd_history = []
            for index, lobj in enumerate(to_do_lobjs):
                if index and index % 10 == 0:
                    save(lobjs)
                print(f"{index + 1}/{len(to_do_lobjs)}")
                add_allohom_info(cmd_history, lobj, [l["id"] for l in to_do_lobjs[index + 1:index + 4]])

            save(lobjs)

        print("Completely done.")

    run_sanhedrin_with_suffixes(go, wordtypes, suffixes)
