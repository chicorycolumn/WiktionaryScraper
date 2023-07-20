from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, show1, \
    user_validate_translations, compare_lobj_id_root
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c, get_curried_save, load_tempsave_if_exists, load_data

if __name__ == '__main__':

    # # # # # #
    wordtype = "ver"
    batch = "01"
    target_lang = "ENG"
    only_run_for_this_many_lobjs = 0  # Only set to integer for testing purposes.
    # # # # # #

    filename = f"{wordtype}_batch_{batch}_SRC"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{filename}_original"
    output_path = f"{stem}{filename}"
    tempsave_path = output_path + "_S02_tempsave"
    save = get_curried_save(output_path, tempsave_path)

    c.print_teal("input_path    =     " + c.teal(input_path))
    c.print_teal("output_path   =     " + c.teal(output_path))
    c.print_teal("tempsave_path =     " + c.teal(tempsave_path))

    doublechecked_src_lobjs = load_tempsave_if_exists(tempsave_path)

    ready = True
    if len(doublechecked_src_lobjs):
        id_of_last_done_src_lobj = doublechecked_src_lobjs[-1]["id"]
        ready = False

    src_lobjs = load_data(input_path)

    if only_run_for_this_many_lobjs:
        src_lobjs = src_lobjs[:only_run_for_this_many_lobjs]
        c.print_bold("BUT FOR TESTING LET'S JUST SAY " + str(len(src_lobjs)))

    for src_lobj_index, src_lobj in enumerate(src_lobjs):
        print("")
        print("")
        print(f"{src_lobj_index + 1}/{len(src_lobjs)}")

        if ready:
            user_validate_translations(src_lobj_index, src_lobj, doublechecked_src_lobjs, save, target_lang)
        else:
            if not ready and compare_lobj_id_root(src_lobj["id"], id_of_last_done_src_lobj):
                print(c.green(src_lobj["id"]), "is last item from tempsave.")
                ready = True
            else:
                print("Already done")

    for lob in doublechecked_src_lobjs:
        if "additionalSpellings" in lob:
            additional_spellings = lob["additionalSpellings"]
        else:
            additional_spellings = []

        for tra in lob["translations"][target_lang]:
            if tra[0] == "+":
                additional_spellings.append(tra[1:])

        if len(additional_spellings):
            print(lob["id"], c.green("added additionalSpellings"), additional_spellings)
            lob["additionalSpellings"] = additional_spellings
            lob["translations"][target_lang] = [t for t in lob["translations"][target_lang] if t[0] != "+"]

    if ready:
        print("")
        print("Done all lobjs, so now doublechecked_src_lobjs has length", len(doublechecked_src_lobjs))

        save(doublechecked_src_lobjs)

        print("Completely done.")
