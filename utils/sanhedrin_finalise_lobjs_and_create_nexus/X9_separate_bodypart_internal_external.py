from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword, run_sanhedrin
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import Color as c, load_data, save

if __name__ == '__main__':

    # # # # # #
    batch = "01"
    # # # # # #

    nex_input_filename = f"nco_batch_{batch}_NEX"
    stem = "./../../output_saved/batches/done/"
    nex_input_path = f"{stem}{nex_input_filename}"

    c.print_teal("nex_input_path    =     " + c.teal(nex_input_path))
    c.print_teal("No tempsave file is used in this stage..")

    nex = load_data(nex_input_path)
    c.print_yellow("Loaded " + nex_input_path)
    print("Loaded", len(nex), "nexus objs.")

    nobs = [nob for nob in nex if 'bodypart' in nob['papers']]

    for index, nob in enumerate(nobs):
        print("")
        print(f'{index+1}/{len(nobs)}')
        if "bodypart" in nob['papers']:
            nob['papers'] = [paper for paper in nob['papers'] if paper != 'bodypart']
            c.print_blue(nob['key'])
            user_input = input("Enter for External,    Any key for Internal: ")
            if not user_input:
                c.print_green('external')
                nob['papers'].append('bodypart external')
            else:
                c.print_yellow('internal')
                nob['papers'].append('bodypart internal')

    save(nex_input_path, None, nex)

    print("Completely done.")
