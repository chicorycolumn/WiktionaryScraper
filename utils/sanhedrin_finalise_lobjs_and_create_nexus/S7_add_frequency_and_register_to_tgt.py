import os

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, get_freq
from utils.postprocessing.common import finalise_lemma_objects, add_tags_and_topics_from_shorthand
from utils.scraping.Polish_dicts import shorthand_tag_refs
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c, get_curried_save, load_data

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    # # # # # #

    input_filename = f"{wordtype}_batch_{batch}_TGT"
    src_input_filename = f"{wordtype}_batch_{batch}_SRC"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"
    tempsave_path = f"{stem}{input_filename}_S7_tempsave"
    src_input_path = f"{stem}{src_input_filename}"
    save = get_curried_save(input_path, tempsave_path)

    c.print_teal("input_path =     " + c.teal(input_path))
    c.print_teal("src_input_path = " + c.teal(src_input_path))
    c.print_teal("tempsave_path = " + c.teal(tempsave_path))
    c.print_teal("Output path will be the same as input.")

    lobjs = []
    src_lobjs = []
    done_lobjs = []

    if os.path.isfile(tempsave_path + ".json"):
        done_lobjs = load_data(tempsave_path)
        c.print_teal("Loaded " + str(len(done_lobjs)) + " items from tempsave.")
        c.print_teal(
            "It's the full number because tempsave records all lobjs, and then we go through the ones which still lack freq and register.")

    else:
        lobjs = load_data(input_path)
        src_lobjs = load_data(src_input_path)

        for lobj in lobjs:
            lobj["register"] = 0
            lobj["frequency"] = 0

            corresponding_src_lobjs = []

            for tran in lobj["»trans"]:
                for sl in src_lobjs:
                    if sl["id"] == tran:
                        corresponding_src_lobjs.append(sl)

            if len(corresponding_src_lobjs) == 1:
                lobj["frequency"] = int(corresponding_src_lobjs[0]["frequency"])
            elif len(set([clob["frequency"] for clob in corresponding_src_lobjs])) == 1:
                lobj["frequency"] = int(corresponding_src_lobjs[0]["frequency"])

            for corresponding_src_lobj in corresponding_src_lobjs:
                if corresponding_src_lobj["register"]:
                    lobj["register"] = int(corresponding_src_lobj["register"])

            done_lobjs.append(lobj)

    lobjs_without_freq = []
    for le in done_lobjs:
        if le["frequency"] == 0:
            print(le["id"])
            lobjs_without_freq.append(le)

    for lindex, lobj in enumerate(lobjs_without_freq):
        if lindex % 10 == 1:
            save(done_lobjs, True)

        print(f"{lindex+1}/{len(lobjs_without_freq)}")
        lobj["frequency"] = get_freq(lobj)

    print("Completely done.")
    save(done_lobjs)
