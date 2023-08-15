from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c, load_data, get_curried_save

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    id_start_number = 1
    reorder_so_siblings_consequent = False
    lang = "src"
    # # # # # #

    input_filename = f"{wordtype}_batch_{batch}_{lang.upper()}"

    stem = "./../../output_saved/batches/done/"

    input_path = f"{stem}{input_filename}"
    save = get_curried_save(input_path, None)

    c.print_teal("input_path    =     " + c.teal(input_path))
    c.print_teal("No tempsave file is used in this stage..")

    lobjs = load_data(input_path)
    c.print_yellow("Loaded " + input_path)
    print("Loaded", len(lobjs), "lobjs.")

    new_lobjs_dict = {}
    for lob in lobjs:
        if lob["lemma"] in new_lobjs_dict:
            new_lobjs_dict[lob["lemma"]].append(lob)
        else:
            new_lobjs_dict[lob["lemma"]] = [lob]

    for tarkey in new_lobjs_dict:
        for lob in new_lobjs_dict[tarkey]:
            if "allohomInfo" in lob and len(new_lobjs_dict[tarkey]) < 2:
                lob.pop("allohomInfo")
                if "(" in lob["id"]:
                    lob["id"] = lob["id"][:lob["id"].index("(")]
            elif "allohomInfo" not in lob and len(new_lobjs_dict[tarkey]) >= 2:
                lob["id"] = lob["id"] + f"(þ)"

    save(lobjs)
