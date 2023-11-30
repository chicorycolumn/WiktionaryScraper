from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword, get_inflections_eng_ver, get_inflections_eng_nou, get_inflections_eng_adj, \
    add_uncountable_label
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import Color as c, get_curried_save, load_tempsave_if_exists, progress_bar, load_data

if __name__ == '__main__':

    # # # # # #
    wordtype = "nco"
    batch = "01"
    # # # # # #

    input_filename = f"{wordtype}_batch_{batch}_TGT"
    stem = "./../../output_saved/batches/done/"
    input_path = f"{stem}{input_filename}"
    tempsave_path = input_path + "_S18_tempsave"
    save = get_curried_save(input_path, tempsave_path)

    c.print_teal("input_path    =     " + c.teal(input_path))
    c.print_teal("tempsave_path =     " + c.teal(tempsave_path))
    c.print_teal("Output path will be the same as input.")

    tgt_lobjs = load_data(input_path)
    results = load_tempsave_if_exists(tempsave_path)
    done_ids = [l['id'] for l in results]

    cmd_history = []

    for index, tgt_lobj in enumerate(tgt_lobjs):
        print('')
        print(f"{index + 1}/{len(tgt_lobjs)}", tgt_lobj['id'][8:])

        if tgt_lobj['id'] not in done_ids:
            add_uncountable_label(tgt_lobj, cmd_history)
            results.append(tgt_lobj)

            if index % 5 == 0:
                save(results, True)
                progress_bar(index + 1, len(tgt_lobjs), True)

    progress_bar(1, 1, True)
    save(results)

    print("")
    print("Completely done.")
