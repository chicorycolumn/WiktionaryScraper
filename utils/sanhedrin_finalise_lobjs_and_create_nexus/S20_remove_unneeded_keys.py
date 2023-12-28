from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q, add_allohom_info, \
    run_sanhedrin
from utils.postprocessing.common import finalise_lemma_objects, add_tags_and_topics_from_shorthand
from utils.scraping.Polish_dicts import shorthand_tag_refs
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import Color as c, get_curried_save, load_data

if __name__ == '__main__':

    # # # # # #
    wordtypes = []  # Leave blank for all.
    batch = "01"
    suffix = "TGT"


    # # # # # #


    def go(wordtype):
        input_filename = f"{wordtype}_batch_{batch}_{suffix}"
        stem = "./../../output_saved/batches/done/"
        input_path = f"{stem}{input_filename}"
        save = get_curried_save(input_path, None)

        c.print_teal("input_path =     " + c.teal(input_path))
        c.print_teal("Output path will be the same as input.")
        c.print_teal("No tempsave files are used for this stage.")

        lobjs = load_data(input_path)

        keys_to_remove = ["translations", "»translations", "tags", "topics"]
        keys_to_move_out_of_inflections = ['lacking', 'tantumPlurale', 'tantumSingulare']
        requires_prefix = ['lacking']
        inflection_keys = ['singular', 'plural']

        child_lobjs = []
        parent_lobjs = []

        for lobj in lobjs:
            # for key_to_remove in keys_to_remove:
            #     lobj.pop(key_to_remove, None)

            if '_inflectionsRoot' in lobj:
                child_lobjs.append(lobj)
            else:
                parent_lobjs.append(lobj)

        for lobj in child_lobjs:
            inflections_source = [x for x in lobjs if x['id'] == lobj['_inflectionsRoot']]

            for key_to_move in keys_to_move_out_of_inflections:
                for inflection_key in inflection_keys:
                    if inflection_key in inflections_source and key_to_move in inflections_source[inflection_key]:
                        value = inflections_source[inflection_key][key_to_move]
                        if key_to_move in requires_prefix:
                            key_to_move = '_' + key_to_move
                        lobj[key_to_move] = value

        for lobj in parent_lobjs:
            for key_to_move in keys_to_move_out_of_inflections:
                for inflection_key in inflection_keys:
                    if inflection_key in lobj['inflections'] and key_to_move in lobj['inflections'][inflection_key]:
                        value = lobj['inflections'][inflection_key].pop(key_to_move)
                        if key_to_move in requires_prefix:
                            key_to_move = '_' + key_to_move
                        lobj[key_to_move] = value

        save(lobjs)

        print("Completely done.")


    run_sanhedrin(go, wordtypes)
