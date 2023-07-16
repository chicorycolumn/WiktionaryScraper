from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, get_signalword, test_signalword
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c, get_curried_save, load_tempsave_if_exists, load_data, deepequals

if __name__ == '__main__':

    # # # # # #
    batch = "01"
    suffix = "SRC"
    wordtype = "nco"
    # # # # # #

    inflection_keys_ref = {
        "adj": ["adverb", "simple", "comparative", "superlative"],
        "nco": ["singular", "plural"],
        "npe": ["singular", "plural"],
    }

    inflection_keys = inflection_keys_ref[wordtype]

    input_filename = f"{wordtype}_batch_{batch}_{suffix}"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"
    save = get_curried_save(input_path, None)

    c.print_teal("input_path    =     " + c.teal(input_path))
    c.print_teal("Output path will be the same as input.")
    c.print_teal("No tempsave file is used for this stage.")

    lobjs = load_data(input_path)
    done_lobjs = []

    for lindex, lobj in enumerate(lobjs):
        reordered_inflections = {}

        for k in lobj["inflections"]:
            if k not in inflection_keys:
                c.print_red(f'Did not expect inflection key "{k}"')
                raise Exception("Stop")

        for k in inflection_keys:
            if k in lobj["inflections"]:
                reordered_inflections[k] = lobj["inflections"][k]

        lobj["inflections"] = reordered_inflections

        done_lobjs.append(lobj)

    save(done_lobjs)

    print("")
    print("Completely done.")
