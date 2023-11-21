from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword, get_inflections_eng_ver, get_inflections_eng_nou, get_inflections_eng_adj
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import Color as c, get_curried_save, load_tempsave_if_exists, progress_bar

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    # # # # # #

    input_filename = f"{wordtype}_batch_{batch}_TGT"
    stem = "./../../output_saved/batches/done/"
    input_path = f"{stem}{input_filename}"
    tempsave_path = input_path + "_S17_tempsave"
    save = get_curried_save(input_path, tempsave_path)

    c.print_teal("input_path    =     " + c.teal(input_path))
    c.print_teal("tempsave_path =     " + c.teal(tempsave_path))
    c.print_teal("Output path will be the same as input.")

    get_inflections_ref = {
        "adj": get_inflections_eng_adj,
        "nco": get_inflections_eng_nou,
        "npe": get_inflections_eng_nou,
        "ver": get_inflections_eng_ver,
    }

    get_inflections = get_inflections_ref[wordtype]

    tgt_lobjs = load_tempsave_if_exists(tempsave_path, input_path)
    siblings = []
    sibling_headers = []

    print("Loaded", len(tgt_lobjs), "target lobjs.")

    for index, tgt_lobj in enumerate(tgt_lobjs):
        print('')
        print(f"{index + 1}/{len(tgt_lobjs)}", tgt_lobj['lemma'])
        if not tgt_lobj.get('inflections'):
            tgt_lobj['inflections'] = get_inflections(tgt_lobj["lemma"])

        if index % 5 == 0:
            save(tgt_lobjs, True)
            progress_bar(index + 1, len(tgt_lobjs), True, True)

    save(tgt_lobjs)

    print("")
    print("Completely done.")
