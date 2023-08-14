from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c, load_data, save

if __name__ == '__main__':

    # # # # # #
    wordtype = "ver"
    batch = "01"
    id_start_number = 1
    reorder_so_siblings_consequent = False
    # # # # # #

    src_input_filename = f"{wordtype}_batch_{batch}_SRC"
    nex_input_filename = f"{wordtype}_batch_{batch}_NEX"

    stem = "./../../output_saved/batches/"

    src_input_path = f"{stem}{src_input_filename}"
    nex_input_path = f"{stem}{nex_input_filename}"

    c.print_teal("src_input_path    =     " + c.teal(src_input_path))
    c.print_teal("nex_input_path    =     " + c.teal(nex_input_path))
    c.print_teal("No tempsave file is used in this stage..")

    src = load_data(src_input_path)
    c.print_yellow("Loaded " + src_input_path)
    nex = load_data(nex_input_path)
    c.print_yellow("Loaded " + nex_input_path)
    
    if reorder_so_siblings_consequent:
        new_lobjs_dict = {}
        for lob in src:
            if lob["lemma"] in new_lobjs_dict:
                new_lobjs_dict[lob["lemma"]].append(lob)
            else:
                new_lobjs_dict[lob["lemma"]] = [lob]
        new_lobjs_list = []
        for tarkey in new_lobjs_dict:
            for lob in new_lobjs_dict[tarkey]:
                new_lobjs_list.append(lob)
        src = new_lobjs_list

    print("Loaded", len(src), "source lobjs.")
    print("Loaded", len(nex), "nexus objs.")

    for slob in src:
        new_id_number = "0000" + str(id_start_number)
        new_id_number = new_id_number[-4:]
        id_start_number += 1

        old_id = slob["id"]
        split = old_id.split("-")
        split[2] = str(new_id_number)
        new_id = "-".join(split)

        slob["id"] = new_id

        for nlob in nex:
            for key in nlob["traductions"]:
                if old_id in nlob["traductions"][key]:
                    new_trans = []
                    for tran in nlob["traductions"][key]:
                        if tran == old_id:
                            new_trans.append(new_id)
                        else:
                            new_trans.append(tran)
                    nlob["traductions"][key] = new_trans

    save(src_input_path, None, src)
    save(nex_input_path, None, nex)

    print("Completely done.")
