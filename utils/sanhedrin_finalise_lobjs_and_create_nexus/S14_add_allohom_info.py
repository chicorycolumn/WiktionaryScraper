from parsers.common import scrape_word_data
from utils.general.common import write_todo
from utils.sanhedrin_finalise_lobjs_and_create_nexus.tools import is_it_the_same_meaning, q
from utils.postprocessing.common import finalise_lemma_objects, add_tags_and_topics_from_shorthand
from utils.scraping.Polish_dicts import shorthand_tag_refs
from utils.scraping.common import check_rescraped_against_existing
from utils.universal import color as c, get_curried_save, load_data

if __name__ == '__main__':

    # # # # # #
    wordtype = "adj"
    batch = "01"
    suffix = "TGT"
    # # # # # #

    templates = {
        "ab": {
            "singleWordtype": True,
            "text": "abstract",
            "emoji": "💭"
        },
        "ph": {
            "singleWordtype": True,
            "text": "physical",
            "emoji": "🪨"
        },
        "pe": {
            "singleWordtype": True,
            "text": "person",
            "emoji": "🏃"
        },
        "ob": {
            "singleWordtype": True,
            "text": "object",
            "emoji": "📦"
        },
        "fo": {
            "singleWordtype": True,
            "text": "food",
            "emoji": "🍲"
        },
        "me": {
            "singleWordtype": True,
            "text": "medical",
            "emoji": "🩺"
        },
        "qu": {
            "singleWordtype": True,
            "text": "quality",
            "emoji": "✅"
        },
        "ma": {
            "singleWordtype": True,
            "text": "mathematical",
            "emoji": "🧮"
        },
        "di": {
            "singleWordtype": True,
            "text": "direction",
            "emoji": "📍"
        },
        "ti": {
            "singleWordtype": True,
            "text": "time",
            "emoji": "🕒"
        },
    }

    input_filename = f"{wordtype}_batch_{batch}_{suffix}"
    stem = "./../../output_saved/batches/"
    input_path = f"{stem}{input_filename}"
    save = get_curried_save(input_path, None)

    c.print_teal("input_path =     " + c.teal(input_path))
    c.print_teal("Output path will be the same as input.")
    c.print_teal("No tempsave files are used for this stage.")

    lobjs = load_data(input_path)

    for lobj in lobjs:
        if "(" in lobj["id"]:


    save(lobjs)

    print("Completely done.")
