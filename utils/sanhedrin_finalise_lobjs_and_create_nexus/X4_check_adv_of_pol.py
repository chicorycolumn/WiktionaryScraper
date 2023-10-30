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
    # # # # # #

    wordtype = "adj"
    input_filename = f"{wordtype}_batch_{batch}_{suffix}"
    tempsave_filename = f"{wordtype}_batch_{batch}_{suffix}_X4_tempsave"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"
    tempsave_path = f"{stem}{tempsave_filename}"
    save = get_curried_save(input_path, tempsave_path)

    c.print_teal("input_path    =     " + c.teal(input_path))
    c.print_teal("tempsave_path =     " + c.teal(tempsave_path))
    c.print_teal("Output path will be the same as input.")

    done_lobjs = load_tempsave_if_exists(tempsave_path)
    lobjs = load_data(input_path)

    for lindex, lobj in enumerate(lobjs):
        print("")
        print(f"{lindex + 1}/{len(lobjs)}")
        print("")

        already_done = False
        for done_lobj in done_lobjs:
            if not already_done and done_lobj["id"] == lobj["id"]:
                print(c.green(done_lobj["id"]), "is last item from tempsave.")
                already_done = True
        if already_done:
            continue

        if lindex % 10 == 0:
            save(done_lobjs, True)

        if "adverb" in lobj["inflections"]:
            c.print_bold(lobj["id"])
            c.print_purple(lobj["inflections"]["adverb"])
            print("")
            conf = not input("OK?   Enter for yes   Any key for no ")
            if conf:
                print("\nOK")
            else:
                del lobj["inflections"]["adverb"]
                print(c.red("Deleted adverb from"), lobj["id"])
        else:
            c.print_blue(lobj["id"])
            c.print_purple("-")
            new_adverb = input("Add adverb? ")
            if new_adverb:
                if new_adverb == "o":
                    new_adverb = lobj["lemma"][:-1] + "o"
                if new_adverb == "e":
                    if lobj["lemma"][-2] == "ł":
                        new_adverb = lobj["lemma"][:-2] + "le"
                    else:
                        new_adverb = lobj["lemma"][:-1] + "ie"
                lobj["inflections"]["adverb"] = new_adverb.strip()
                print(c.green(lobj["inflections"]["adverb"]), "added to", lobj["id"])

        done_lobjs.append(lobj)

    save(done_lobjs)

    print("")
    print("Completely done.")
