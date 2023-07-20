import os

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, get_freq, get_new_freqs
from utils.postprocessing.common import finalise_lemma_objects, add_tags_and_topics_from_shorthand
from utils.scraping.Polish_dicts import shorthand_tag_refs
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c, get_curried_save, load_data

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    step = 2  # Step 1 to record changes. Step 2 to apply changes.
    # # # # # #

    input_filename = f"{wordtype}_batch_{batch}_TGT"
    src_input_filename = f"{wordtype}_batch_{batch}_SRC"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"
    tempsave_path = f"{stem}{input_filename}_S09_tempsave"
    src_input_path = f"{stem}{src_input_filename}"
    save = get_curried_save(input_path, tempsave_path)

    c.print_teal("input_path =     " + c.teal(input_path))
    c.print_teal("src_input_path = " + c.teal(src_input_path))
    c.print_teal("tempsave_path = " + c.teal(tempsave_path))
    c.print_teal("Output path will be the same as input.")

    lobjs = load_data(input_path)
    sorted_lobjs = {}
    to_change_lobjs = {
        "F1": [],
        "F2": [],
        "F3": [],
        "F4": [],
        "F5": [],
        "F1 done up to": 0,
        "F2 done up to": 0,
        "F3 done up to": 0,
        "F4 done up to": 0,
        "F5 done up to": 0,
    }

    if os.path.isfile(tempsave_path + ".json"):
        to_change_lobjs = load_data(tempsave_path)
        c.print_teal("Loaded " + str(len(to_change_lobjs)) + " items from tempsave.")

    if step == 1:
        sorted_lobjs["F1"] = [l for l in lobjs if int(l["frequency"]) == 1]
        sorted_lobjs["F2"] = [l for l in lobjs if int(l["frequency"]) == 2]
        sorted_lobjs["F3"] = [l for l in lobjs if int(l["frequency"]) == 3]
        sorted_lobjs["F4"] = [l for l in lobjs if int(l["frequency"]) == 4]
        sorted_lobjs["F5"] = [l for l in lobjs if int(l["frequency"]) == 5]

        print("")
        for num in [1,2,3,4,5]:
            print("")
            print("")
            print(len(sorted_lobjs["F" + str(num)]), f"lobjs with frequency category {str(num)}.")

            temp_arr = []

            for lebindex, leb in enumerate(sorted_lobjs["F" + str(num)]):
                if to_change_lobjs[f"F{str(num)} done up to"] > 0 and lebindex <= to_change_lobjs[f"F{str(num)} done up to"]:
                    print("Already done", lebindex)
                    continue

                if lebindex != 0 and ((lebindex + 1 == len(sorted_lobjs["F" + str(num)])) or (lebindex % 10 == 0)):
                    temp_arr.append([lebindex, leb])

                    c.print_purple(f'Are these frequency category {str(num)}?')
                    for ho in temp_arr:
                        printable_lebindex = f"{' ' if ho[0] < 10 else ''}{ho[0]}"
                        print(c.bold(printable_lebindex), c.blue(ho[1]["id"]), ho[1]["»trans"])
                    c.print_purple(f'Are these frequency category {str(num)}?')
                    print("")

                    requested_changes = get_new_freqs(temp_arr)

                    for requested_change in requested_changes:
                        new_freq = requested_change[0]
                        id_of_lobj_to_change = requested_change[1]
                        to_change_lobjs[f"F{str(new_freq)}"].append(id_of_lobj_to_change)

                    to_change_lobjs[f"F{str(num)} done up to"] = lebindex
                    save(to_change_lobjs, True)
                    temp_arr = []
                else:
                    temp_arr.append([lebindex, leb])

            save(to_change_lobjs, True)
    elif step == 2:
        for num in [1,2,3,4,5]:
            ids_of_lobjs_to_change = to_change_lobjs[f"F{str(num)}"]
            print(len(ids_of_lobjs_to_change), "lobjs to change to frequency", c.bold(str(num)))

            for ids_of_lobj_to_change in ids_of_lobjs_to_change:
                for lobj in lobjs:
                    if lobj["id"] == ids_of_lobj_to_change:
                       lobj["frequency"] = num

        print("Completely done.")
        save(lobjs)
