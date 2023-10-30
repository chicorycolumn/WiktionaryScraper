from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q
from utils.postprocessing.common import finalise_lemma_objects, add_tags_and_topics_from_shorthand
from utils.scraping.Polish_dicts import shorthand_tag_refs
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import Color as c, save, load_data

if __name__ == '__main__':

    # # # # # #
    wordtype = "ver"
    batch = "01"
    input_filenames = ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
    # # # # # #

    folder_ref = {
        "nou": "nouns",
        "adj": "adjectives",
        "ver": "verbs",
    }

    input_folder = folder_ref[wordtype]
    input_filenames = [f"{input_folder}_{input_filename}" for input_filename in input_filenames]
    input_stem = f"./../../output_saved/{input_folder}/"

    output_stem = f"./../../output_saved/batches/"
    output_filename = f"{wordtype}_batch_{batch}_SRC_original"
    output_path = f"{output_stem}{output_filename}"

    c.print_teal("output_path =     " + c.teal(output_path))
    c.print_teal("No tempsave files are used for this stage.")

    all_src_lobjs = []

    for input_filename in input_filenames:
        input_path = f"{input_stem}{input_filename}"
        c.print_teal("input_path =      " + c.teal(input_path))
        src_lobjs = load_data(input_path)
        all_src_lobjs.extend(src_lobjs)

    print("Total all_src_lobjs", len(all_src_lobjs))

    if wordtype == "nou":
        npe = []
        nco = []
        for lobj in all_src_lobjs:
            if lobj["id"].split("-")[1] == "npe":
                npe.append(lobj)
            elif lobj["id"].split("-")[1] == "nco":
                nco.append(lobj)
            else:
                raise Exception("Wordtype not in ['nco', 'npe'] of lobj " + lobj["id"])

        npe_output_filename = f"npe_batch_{batch}_SRC_original"
        npe_output_path = f"{output_stem}{npe_output_filename}"

        nco_output_filename = f"nco_batch_{batch}_SRC_original"
        nco_output_path = f"{output_stem}{nco_output_filename}"

        save(npe_output_path, None, npe)
        save(nco_output_path, None, nco)
    else:
        save(output_path, None, all_src_lobjs)

    print("Completely done.")
