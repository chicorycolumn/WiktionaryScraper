import json
import os
import time

from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, get_freq, get_new_freqs
from utils.postprocessing.common import finalise_lemma_objects, add_tags_and_topics_from_shorthand
from utils.scraping.Polish_dicts import shorthand_tag_refs
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    step = 1  # Step 1 to record changes. Step 2 to apply changes.
    # # # # # #

    input_filename = f"{wordtype}_batch_{batch}_TGT"
    src_input_filename = f"{wordtype}_batch_{batch}_SRC"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"
    tempsave_path = f"{stem}{input_filename}_S8_tempsave"
    src_input_path = f"{stem}{src_input_filename}"

    c.print_teal("input_path =     " + c.teal(input_path))
    c.print_teal("src_input_path = " + c.teal(src_input_path))
    c.print_teal("tempsave_path = " + c.teal(tempsave_path))
    c.print_teal("Output path will be the same as input.")

    def save(data, temp: bool = False):
        print(f"📀 {'SAVING FINAL'}")

        _output_path = tempsave_path if temp else input_path

        with open(_output_path + ".json", "w") as outfile:
            print(f'Writing {len(data)} results.')
            data_json = json.dumps(data, indent=2, ensure_ascii=False)
            outfile.write(data_json)
            outfile.close()

    lobjs = []
    sorted_lobjs = {}
    to_change_lobjs = {}

    to_change_lobjs["F1"] = []
    to_change_lobjs["F2"] = []
    to_change_lobjs["F3"] = []
    to_change_lobjs["F4"] = []
    to_change_lobjs["F5"] = []

    to_change_lobjs["F1 done up to"] = 0
    to_change_lobjs["F2 done up to"] = 0
    to_change_lobjs["F3 done up to"] = 0
    to_change_lobjs["F4 done up to"] = 0
    to_change_lobjs["F5 done up to"] = 0

    with open(input_path + ".json", "r") as f:
        lobjs = json.load(f)
        print("Loaded", len(lobjs), "lobjs.")
        f.close()

    if os.path.isfile(tempsave_path + ".json"):
        with open(tempsave_path + ".json", "r") as f:
            to_change_lobjs = json.load(f)
            c.print_teal("Loaded " + str(len(to_change_lobjs)) + " items from tempsave.")
            f.close()

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

            if lebindex != 0 and ((lebindex + 1 == len(sorted_lobjs["F" + str(num)])) or (lebindex % 20 == 0)):
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

    # user_input = input("Which frequency category do you want to check? 1-5 ")
    #
    # if user_input and user_input in "12345":
    #     freq_to_check = user_input
    #     lobjs_to_check = sorted_lobjs["F" + str(freq_to_check)]
    #     for lindex, lob in enumerate(lobjs_to_check):
    #         print(f"{lindex+1}/{len(lobjs_to_check)}")
    #         print(f'{c.purple(lob["lemma"])} {c.blue(lob["id"])}')
    #         user_input = get_freq(lob, f"{freq_to_check} OK?   Enter for yes   Or enter new frequency ", True)
    #         if user_input:
    #             lob["frequency"] = int(user_input)
    #
    print("Completely done.")
    save(lobjs)
