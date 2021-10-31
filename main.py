from input.Polish.nouns.head_words import input as nouns
from input.Polish.adjectives.head_words import input as adjectives
from input.Polish.verbs.head_words import input as verbs
from parsers.common import scrape_word_data
from utils.postprocessing.common import make_ids, finalise_lemma_objects

if __name__ == '__main__':
    # Note! Manually check all feminine nouns to see if add "isPerson": True.

    step = 1
    wordtype = "nouns"
    group_number = 1
    input_indexes = [0, 100]

    skip_make_ids = False
    skip_scraping = False
    these_headwords_only = []

    """
    
    Step 1: scrape_word_data()
                        output_*_99_scraped CREATED (ignore unless next fxn encounters error)
                        rejected_*_99 CREATED
                generate_adjective()/minimise_verbs()
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

    head_words = these_headwords_only if these_headwords_only \
        else head_words_ref[wordtype][input_indexes[0]:input_indexes[1]]

    if not skip_make_ids:
        make_ids(wordtype, group_number)
        pass
    elif step == 1:
        scrape_word_data(
            group_number=group_number,
            head_words=head_words,
            wordtype=wordtype,
            language="Polish",
            skip_scraping=skip_scraping
        )
    elif step == 3:
        finalise_lemma_objects(group_number, wordtype)