from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword, run_sanhedrin, check_all_inflections_begin_with
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import Color as c, get_curried_save, load_tempsave_if_exists, load_data, deepequals

if __name__ == '__main__':

    # # # # # #
    wordtypes = []  # Leave blank for all.
    batch = "01"
    suffix_and_lang = []  # ['SRC', 'pol']
    # # # # # #

    def go(wordtype, suffix, lang):
        input_filename = f"{wordtype}_batch_{batch}_{suffix}"
        stem = f"output_saved/batches/{'done/'}"
        input_path = f"{stem}{input_filename}"
        input_path = "./../../" + input_path

        c.print_teal("input_path    =     " + c.teal(input_path))
        c.print_teal("Output path will be the same as input.")
        c.print_teal("No tempsave file is used for this stage.")

        lobjs = load_data(input_path)

        for lindex, lobj in enumerate(lobjs):
            if '_inflectionsRoot' in lobj:
                parent_lobj = [l for l in lobjs if l['id'] == lobj['_inflectionsRoot']][0]
                lobj['inflections'] = parent_lobj['inflections']
                lobj.pop('_inflectionsRoot')
            result_bool = check_all_inflections_begin_with(lobj)
            # if result_bool:
            #     c.print_green(f'{lindex + 1}/{len(lobjs)} {lobj["lemma"]}')


        print("")
        print("Completely done.")


    if not len(suffix_and_lang):
        run_sanhedrin(go, wordtypes, ['SRC', 'pol'])
        run_sanhedrin(go, wordtypes, ['TGT', 'eng'])
    else:
        run_sanhedrin(go, wordtypes, suffix_and_lang)
