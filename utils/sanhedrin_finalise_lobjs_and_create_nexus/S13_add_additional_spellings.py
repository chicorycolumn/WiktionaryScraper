from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q
from utils.postprocessing.common import finalise_lemma_objects, add_tags_and_topics_from_shorthand
from utils.scraping.Polish_dicts import shorthand_tag_refs
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c, get_curried_save, load_data

if __name__ == '__main__':

    # # # # # #
    wordtype = "npe"
    batch = "01"
    suffix = "TGT"
    # # # # # #

    additional_spelling_sets = {
        "adj": [],
        "npe": [
            ["neighbour", "neighbor"],
        ],
        "nco": [
            ["mathematics", "math", "maths"],
            ["kilogram", "kilo"],
            ["colour", "color"],
            ["metre", "meter"],
            ["axe", "ax"],
            ["kilometre", "kilometer"],
            ["photograph", "photo"],
            ["litre", "liter"],
            ["crossroad", "crossroads"],
            ["bicycle", "bike"],
            ["storey", "story"],
            ["centre", "center"],
            ["advertisement", "advert", "ad"],
            ["fridge", "refrigerator"],
            ["launderette", "laundrette"],
            ["odour", "odor"],
            ["sulphur", "sulfur"],
            ["theatre", "theater"],
            ["mould", "mold"],
            ["doughnut", "donut"],
            ["neighbourhood", "neighborhood"],
            ["behaviour", "behavior"],
            ["laboratory", "lab"],
        ],
    }

    input_filename = f"{wordtype}_batch_{batch}_{suffix}"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"
    save = get_curried_save(input_path, None)

    c.print_teal("input_path =     " + c.teal(input_path))
    c.print_teal("Output path will be the same as input.")
    c.print_teal("No tempsave files are used for this stage.")

    lobjs = load_data(input_path)

    for spelling_set in additional_spelling_sets:
        done = False
        for lobj in lobjs:
            if lobj["lemma"] == spelling_set[0]:
                if "additionalSpellings" in lobj:
                    additional_spellings = lobj["additionalSpellings"]
                else:
                    additional_spellings = []
                additional_spellings.extend(spelling_set[1:])
                done = True
        if not done:
            print(c.red("No lobj found for spelling set:"), spelling_set[0])
            raise Exception("Stop")

    save(lobjs)

    print("Completely done.")
