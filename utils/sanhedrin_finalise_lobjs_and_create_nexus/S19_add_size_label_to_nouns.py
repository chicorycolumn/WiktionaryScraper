from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword, get_inflections_eng_ver, get_inflections_eng_nou, get_inflections_eng_adj, \
    add_size_tag
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import Color as c, get_curried_save, load_tempsave_if_exists, progress_bar, load_data

if __name__ == '__main__':

    # # # # # #
    batch = "01"
    # # # # # #

    wordtype = "nco"
    input_filename = f"{wordtype}_batch_{batch}_NEX"
    stem = "./../../output_saved/batches/done/"
    input_path = f"{stem}{input_filename}"
    tempsave_path = input_path + "_S19_tempsave"
    save = get_curried_save(input_path, tempsave_path)

    c.print_teal("input_path    =     " + c.teal(input_path))
    c.print_teal("tempsave_path =     " + c.teal(tempsave_path))
    c.print_teal("Output path will be the same as input.")

    nex_lobjs = load_data(input_path)
    results = load_tempsave_if_exists(tempsave_path)
    done_ids = [l['key'] for l in results]

    cmd_history = []

    def print_simple_status(index, lobjs, lobj, done: bool = False):
        lem = lobj['key'][9:]
        print(f"{index + 1}/{len(lobjs)}", c.green(lem) if done else c.blue(lem))

    counter = 0
    for index, nex_lobj in enumerate(nex_lobjs):
        print('')

        if nex_lobj['key'] in done_ids:
            print_simple_status(index, nex_lobjs, nex_lobj, done=True)
        else:
            counter += 1
            print_simple_status(index, nex_lobjs, nex_lobj)
            add_size_tag(nex_lobj, cmd_history)
            results.append(nex_lobj)

            if counter % 5 == 0:
                save(results, True)
                progress_bar(index + 1, len(nex_lobjs), True)

    save(results, True)
    progress_bar(1, 1, True)
    save(results)

    print("")
    print("Completely done.")
