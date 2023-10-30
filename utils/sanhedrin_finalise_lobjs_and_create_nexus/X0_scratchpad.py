from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import Color as c, get_curried_save, load_tempsave_if_exists, load_data, deepequals

if __name__ == '__main__':

    # # # # # #
    batch = "01"
    suffix = "SRC"
    wordtype = "adj"
    # # # # # #

    input_filename = f"{wordtype}_batch_{batch}_{suffix}"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"
    save = get_curried_save(input_path, None)

    c.print_teal("input_path    =     " + c.teal(input_path))

    lobjs = load_data(input_path)
    res = []

    for lindex, lobj in enumerate(lobjs):
        if "adverb" in lobj["inflections"]:
            res.append(lobj["lemma"])

    res = list(set(res))

    print(len(res), "res items.")
    for el in res:
        print(f'"{el}",')

    print("Completely done.")
