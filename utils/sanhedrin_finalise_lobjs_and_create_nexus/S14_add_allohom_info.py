from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_allohom_info, \
    run_sanhedrin_with_suffixes
from utils.postprocessing.common import finalise_lemma_objects, add_tags_and_topics_from_shorthand
from utils.scraping.Polish_dicts import shorthand_tag_refs
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import Color as c, get_curried_save, load_data

if __name__ == '__main__':

    # # # # # #
    wordtypes = ['nco']  # Leave blank for all.
    batch = "01"
    suffixes = []  # Leave blank for both SRC and TGT.
    just_list_them = False  # Should be False


    # # # # # #

    def add_missing_allohom_info(wordtype, suffix):
        input_filename = f"{wordtype}_batch_{batch}_{suffix}"
        stem = "./../../output_saved/batches/done/"
        input_path = f"{stem}{input_filename}"
        save = get_curried_save(input_path, None)

        c.print_teal("input_path =     " + c.teal(input_path))
        c.print_teal("Output path will be the same as input.")
        c.print_teal("No tempsave files are used for this stage.")

        lobjs = load_data(input_path)

        to_do_lobjs = []
        for lobj in lobjs:
            if "(" in lobj["id"]:
                if "allohomInfo" not in lobj or not lobj["allohomInfo"]:
                    to_do_lobjs.append(lobj)

        c.print_bold(f"{len(to_do_lobjs)} need allohomInfo added.")
        if just_list_them:
            for l in to_do_lobjs:
                print(l['id'])
            print('')
        else:
            cmd_history = []
            for index, lobj in enumerate(to_do_lobjs):
                if index and index % 10 == 0:
                    save(lobjs)
                print(f"{index + 1}/{len(to_do_lobjs)}")
                add_allohom_info(cmd_history, lobj, [l["id"] for l in to_do_lobjs[index + 1:index + 4]])

            save(lobjs)

        print("Completely done.")


    def flag_any_other_required_allohom(wordtype, suffix, round):
        lang = suffix
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
                    if round == 1 and ('allohomInDifferentWordtype' not in lob['allohomInfo'] or not lob['allohomInfo']['allohomInDifferentWordtype']):
                        c.print_red(f'{lob["id"]}   REMOVING ALLOHOM INFO')
                        lob.pop("allohomInfo")
                    if "(" in lob["id"]:
                        lob["id"] = lob["id"][:lob["id"].index("(")]
                elif "allohomInfo" not in lob and len(new_lobjs_dict[tarkey]) >= 2:
                    lob["id"] = lob["id"] + f"(þ)"

        save(lobjs)


    def run_both(round):
        c.print_purple('ADDING ANY NECESSARY FLAGS')
        run_sanhedrin_with_suffixes(flag_any_other_required_allohom, wordtypes, suffixes, [round])
        c.print_purple('FINISHED ANY NECESSARY FLAGS')

        print('')

        c.print_blue('READY TO ADD ALLOHOM INFO FROM USER INPUT')
        run_sanhedrin_with_suffixes(add_missing_allohom_info, wordtypes, suffixes)
        c.print_blue('READY TO ADD ALLOHOM INFO FROM USER INPUT')


    c.print_bold('- - - - -')
    c.print_bold('PHASE 1/2')
    c.print_bold('- - - - -')
    run_both(round=1)
    c.print_bold('- - - - -')
    c.print_bold('PHASE 2/2')
    c.print_bold('- - - - -')
    run_both(round=2)