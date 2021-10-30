from utils.general.common import *
from utils.scraping.common import *
from utils.scraping.Polish import *
from utils.postprocessing.common import *
from utils.postprocessing.Polish import *
from parsers.common import *

from input.Polish.nouns.head_words import input as nouns
from input.Polish.adjectives.head_words import input as adjectives
from input.Polish.verbs.head_words import input as verbs


if __name__ == '__main__':
    # Note! Manually check all feminine nouns to see if add "isPerson": True.

    wordtype = "verbs"
    group_number = 333
    run_make_ids = False

    input_indexes = [0, 5]
    step = 3
    scraping_already_done = False

    """
    Nouns: Group1: 0-50, Group2: 50-100
    
    Step 1: scrape_word_data()
                        output_*_99_scraped CREATED (ignore unless next fxn encounters error)
                        rejected_*_99 CREATED
                generate_adjectives()/minimise_verbs()
                        output_*_99 CREATED
                        truncated_*_99 CREATED

    Step 2: Move the three files to output_saved; manually add shorthand tags; whittle translations.
                        truncated_*_99 MODIFIED

    Step 3: finalise_lemma_objects()
                untruncate_lemma_objects()
                        untruncated_*_99 CREATED
                expand_tags_and_topics()
                        finished_*_99 CREATED             
    """

    head_words_ref = {
        "adjectives": adjectives,
        "nouns": nouns,
        "verbs": verbs
    }
    input_list = head_words_ref[wordtype]
    head_words = input_list[input_indexes[0]:input_indexes[1]]

    if run_make_ids:
        make_ids(wordtype, group_number)
        pass
    elif step == 1:
        scrape_word_data(
            group_number=group_number,
            head_words=head_words,
            wordtype=wordtype,
            language="Polish",
            scraping_already_done=scraping_already_done
        )
    elif step == 3:
        finalise_lemma_objects(group_number, wordtype)