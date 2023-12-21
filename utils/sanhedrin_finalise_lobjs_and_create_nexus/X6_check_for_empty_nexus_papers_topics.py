from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword, run_sanhedrin
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import Color as c, load_data, save

if __name__ == '__main__':

    # # # # # #
    wordtypes = []  # Leave blank for all.
    batch = "01"
    # # # # # #

    def go(wordtype):
        nex_input_filename = f"{wordtype}_batch_{batch}_NEX"
        stem = "./../../output_saved/batches/done/"
        nex_input_path = f"{stem}{nex_input_filename}"

        c.print_teal("nex_input_path    =     " + c.teal(nex_input_path))
        c.print_teal("No tempsave file is used in this stage..")

        nex = load_data(nex_input_path)
        c.print_yellow("Loaded " + nex_input_path)

        print("Loaded", len(nex), "nexus objs.")

        res = {
            'no papers key': [],
            'no topics key': [],
            'no papers': [],
            'no topics': [],
        }

        for nobj in nex:
            if 'papers' not in nobj:
                res['no papers key'].append(nobj['key'])
            if 'topics' not in nobj:
                res['no topics key'].append(nobj['key'])
            if len(nobj['papers']) == 0:
                res['no papers'].append(nobj['key'])
            if len(nobj['topics']) == 0:
                res['no topics'].append(nobj['key'])

        for key in res.keys():
            c.print_blue(f"{len(res[key])} {key}")

        if all(len(res[key]) == 0 for key in res.keys()):
            print("🟢 All resolved.")


    run_sanhedrin(go, wordtypes)
