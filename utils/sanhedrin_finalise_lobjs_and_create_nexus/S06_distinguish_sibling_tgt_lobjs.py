from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, get_signalword, test_signalword
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c, get_curried_save, load_tempsave_if_exists

if __name__ == '__main__':

    # # # # # #
    wordtype = "nco"
    batch = "01"
    target_lang = "ENG"
    # # # # # #

    input_filename = f"{wordtype}_batch_{batch}_SRC"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"
    tempsave_path = input_path + "_S06_tempsave"
    _save = get_curried_save(input_path, tempsave_path)

    c.print_teal("input_path    =     " + c.teal(input_path))
    c.print_teal("tempsave_path =     " + c.teal(tempsave_path))
    c.print_teal("Output path will be the same as input.")

    def save(tgt_lobjs, temp: bool = False):
        print(f"Got {len(tgt_lobjs)} members.")
        print("Reordering so siblings are next to each other...")
        res = []
        done_ids = []
        for l in tgt_lobjs:
            if l["id"] not in done_ids:
                is_sibling = False
                for sib_set in siblings:
                    if sib_set[0]["id"] == l["id"]:
                        if is_sibling:
                            raise Exception(f'Why is there more than one sibling set for "{l["id"]}"?')
                        is_sibling = True
                        res.extend(sib_set)
                        done_ids.extend([lo["id"] for lo in sib_set])

                if l["id"] in all_sibling_ids:  # Catching the ones that got deleted, don't add to res.
                    is_sibling = True
                    done_ids.append(l["id"])

                if not is_sibling:
                    res.append(l)
                    done_ids.append(l["id"])
        print(f"Got {len(res)} members.")

        _save(res, temp)

    tgt_lobjs = load_tempsave_if_exists(tempsave_path, input_path)
    siblings = []
    sibling_headers = []

    print("Loaded", len(tgt_lobjs), "target lobjs.")

    for index_1, tgt_lobj_1 in enumerate(tgt_lobjs):
        if tgt_lobj_1["lemma"] not in sibling_headers:
            sibling_set = [tgt_lobj_1]
            for index_2, tgt_lobj_2 in enumerate(tgt_lobjs):
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
        signalwords = [get_signalword(l["id"]) for l in sib_set]
        failed = False
        for signalword in signalwords:
            if not test_signalword(signalword):
                failed = True

        print("")
        print(f"{sib_set_index + 1}/{len(siblings)}")

        if not failed:
            c.print_green("ALREADY LOOKS DONE")
            for sibl in sib_set:
                print(c.green(get_signalword(sibl["id"])), sibl)
            continue

        if sib_set_index % 5 == 0:
            save(tgt_lobjs, True)

        add_signalwords(sib_set)

    save(tgt_lobjs)

    print("")
    print("Completely done.")
