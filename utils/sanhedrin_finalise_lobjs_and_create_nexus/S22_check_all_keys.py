from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_signalwords, \
    get_signalword, test_signalword, run_sanhedrin
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import Color as c, get_curried_save, load_tempsave_if_exists, load_data, deepequals

if __name__ == '__main__':

    # # # # # #
    wordtypes = []  # Leave blank for all.
    batch = "01"
    suffix_and_lang = []  # ['SRC', 'pol']


    # # # # # #

    def go(wordtype, suffix, lang):
        inflection_keys_ref = {
            "adj": ["adverb", "simple", "comparative", "superlative"],
            "nco": ["singular", "plural"],
            "npe": ["singular", "plural"],
            "ver": [
                "infinitive",
                "verbalNoun",
                "activeAdjectival",
                "passiveAdjectival",
                "contemporaryAdverbial",
                "anteriorAdverbial",
                "verbal"
            ],
            "verbal": [
                "conditional",
                "future",
                "imperative",
                "past",
                "present",
            ]
        }

        lobj_keys_ref = {
            "adj": {
                'mandatory': ["lemma", "id", "frequency", "register", "inflections", ],
                'optional': ["_inflectionsRoot", "_untranslated", "_lacking", "allohomInfo", "extra",
                             "additionalSpellings"],
            },
            "nco": {
                'mandatory': ["lemma", "id", "frequency", "register", "inflections",
                              "gender" if lang in ['pol'] else None, ],
                'optional': ["_inflectionsRoot", "_untranslated", "_lacking", "allohomInfo", "extra",
                             "additionalSpellings", "tantumSingulare",
                             "tantumPlurale", ],
            },
            "npe": {
                'mandatory': ["lemma", "id", "frequency", "register", "inflections",
                              "gender" if lang in ['pol'] else None, ],
                'optional': ["_inflectionsRoot", "_untranslated", "_lacking", "allohomInfo", "extra",
                             "additionalSpellings", ],
            },
            "ver": {
                'mandatory': ["lemma", "id", "frequency", "register", "inflections",
                              "aspect" if lang in ['pol'] else None, ],
                'optional': ["_inflectionsRoot", "_untranslated", "_lacking", "allohomInfo", "extra",
                             "additionalSpellings",
                             "secondaryAspects"],
            }
        }

        inflection_keys = inflection_keys_ref[wordtype]
        lobj_keys = lobj_keys_ref[wordtype]

        input_filename = f"{wordtype}_batch_{batch}_{suffix}"
        stem = f"output_saved/batches/{'done/'}"
        input_path = f"{stem}{input_filename}"
        input_path = "./../../" + input_path
        save = get_curried_save(input_path, None)

        c.print_teal("input_path    =     " + c.teal(input_path))
        c.print_teal("Output path will be the same as input.")
        c.print_teal("No tempsave file is used for this stage.")

        lobjs = load_data(input_path)

        for lindex, lobj in enumerate(lobjs):
            if 'inflections' in lobj and '_inflectionsRoot' in lobj:
                print(lobj['id'])
                c.print_purple("can't have both inflections & _inflectionsRoot")
            for mandatory_lobj_key in [k for k in lobj_keys['mandatory'] if k]:
                if mandatory_lobj_key not in lobj:
                    if not (mandatory_lobj_key == 'inflections' and '_inflectionsRoot' in lobj):
                        print(lobj['id'])
                        c.print_blue("missing " + mandatory_lobj_key)
            for lobj_key in lobj:
                if lobj_key not in lobj_keys['mandatory'] and lobj_key not in lobj_keys['optional']:
                    print(lobj['id'])
                    c.print_red("unexpected " + lobj_key)

        print("")
        print("Completely done.")


    if not len(suffix_and_lang):
        run_sanhedrin(go, wordtypes, ['SRC', 'pol'])
        run_sanhedrin(go, wordtypes, ['TGT', 'eng'])
    else:
        run_sanhedrin(go, wordtypes, suffix_and_lang)
