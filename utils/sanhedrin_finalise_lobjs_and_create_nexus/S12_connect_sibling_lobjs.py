from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c, get_curried_save, load_tempsave_if_exists, load_data, deepequals

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    suffix = "SRC"
    # # # # # #

    input_filename = f"{wordtype}_batch_{batch}_{suffix}"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"
    save = get_curried_save(input_path, None)

    c.print_teal("input_path    =     " + c.teal(input_path))
    c.print_teal("Output path will be the same as input.")
    c.print_teal("No tempsave file is used for this stage.")

    lobjs = load_data(input_path)
    siblings = []
    sibling_headers = []

    for index_1, tgt_lobj_1 in enumerate(lobjs):
        if tgt_lobj_1["lemma"] not in sibling_headers:
            sibling_set = [tgt_lobj_1]
            for index_2, tgt_lobj_2 in enumerate(lobjs):
                if index_1 != index_2 and tgt_lobj_1["lemma"] == tgt_lobj_2["lemma"]:
                    sibling_set.append(tgt_lobj_2)
            if len(sibling_set) > 1:
                siblings.append(sibling_set)
                sibling_headers.append(tgt_lobj_1["lemma"])

    all_sibling_ids = []  # Some may get deleted but their IDs  kept here so don't put them back into res when saving.
    print(f"There are {len(siblings)} sibling sets.")
    for sib_set in siblings:
        print(sib_set)
        for sibli in sib_set:
            all_sibling_ids.append(sibli["id"])

    print(f"There are {len(siblings)} sibling sets.")
    for sib_set_index, sib_set in enumerate(siblings):
        print("")
        print(f"{sib_set_index + 1}/{len(siblings)}")

        root_id_for_inflections = None

        for sindex, sibling_b in enumerate(sib_set):
            if sindex == 0:
                root_id_for_inflections = sibling_b["id"]
                continue

            sibling_a = sib_set[sindex - 1]

            same_exact_inflections = deepequals(sibling_a["inflections"], sibling_b["inflections"])

            print(c.blue(sibling_a["id"]), sibling_a)
            print(c.blue(sibling_b["id"]), sibling_b)
            c.print_bold("SAME" if same_exact_inflections else "DIFFERENT")
            print("")

            if same_exact_inflections:
                sibling_b["inflectionsRoot"] = root_id_for_inflections

        for sindex, sibling_b in enumerate(sib_set):
            if "inflectionsRoot" in sibling_b:
                if sindex == 0:
                    c.print_red("Didn't expect first sibling to have inflectionsRoot key: " + sibling_b["id"])
                    raise Exception("Stop")

                del sibling_b["inflections"]

    save(lobjs)

    print("")
    print("Completely done.")
