from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c, get_curried_save, load_tempsave_if_exists, load_data, deepequals

if __name__ == '__main__':

    # # # # # #
    batch = "01"
    suffix = "SRC"
    wordtype = "ver"
    # # # # # #

    inflection_keys_ref = {
        "adj": ["adverb", "simple", "comparative", "superlative"],
        "nco": ["singular", "plural"],
        "npe": ["singular", "plural"],
        "ver": [
            "infinitive",
            "verbalNoun",
            "activeAdjectival",
            "passiveAdjectival",
            "contemporaryAdverbial",
            "anteriorAdverbial",
            "verbal"
        ],
        "verbal": [
            "conditional",
            "future",
            "imperative",
            "past",
            "present",
        ]
    }

    lobj_keys_ref = {
        "ver": ["lemma", "id", "aspect", "secondaryAspects", "tags", "topics", "frequency", "register", "allohomInfo",
                "inflections", "translations", "extra", "derivedTerms", "otherShapes"]
    }

    move_these_keys_to_extra = ["derivedTerms", "otherShapes"]

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

        if wordtype == "ver":
            reordered_verbal_inflections = {}

            for k in lobj["inflections"]["verbal"]:
                if k not in inflection_keys_ref["verbal"]:
                    c.print_red(f'Did not expect inflection key "{k}"')
                    raise Exception("Stop")

            for k in inflection_keys_ref["verbal"]:
                if k in lobj["inflections"]["verbal"]:
                    reordered_verbal_inflections[k] = lobj["inflections"]["verbal"][k]

            lobj["inflections"]["verbal"] = reordered_verbal_inflections

        done_lobjs.append(lobj)

    if wordtype in lobj_keys_ref:
        double_done_lobjs = []

        inflection_keys = lobj_keys_ref[wordtype]
        for lindex, lobj in enumerate(done_lobjs):
            reordered_lobj = {}

            for k in lobj:
                if k not in inflection_keys:
                    c.print_red(f'Did not expect lobj key "{k}"')
                    raise Exception("Stop")

            for k in inflection_keys:
                if k in lobj:

                    if k in move_these_keys_to_extra:
                        if "extra" not in reordered_lobj:
                            reordered_lobj["extra"] = {}
                        if k in reordered_lobj["extra"]:
                            print("Woah", reordered_lobj["id"], k)
                        else:
                            reordered_lobj["extra"][k] = lobj[k]
                    else:
                        reordered_lobj[k] = lobj[k]

            double_done_lobjs.append(reordered_lobj)

        save(double_done_lobjs)
    else:
        save(done_lobjs)

    print("")
    print("Completely done.")
