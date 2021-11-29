from input.Polish.nouns.head_words import input as nouns
from input.Polish.adjectives.head_words import input as adjectives
from input.Polish.verbs.head_words import input as verbs
from parsers.common import scrape_word_data
from utils.postprocessing.common import make_ids, finalise_lemma_objects

if __name__ == '__main__':

    step = 2
    wordtype = "nouns"
    group_number = 333
    input_indexes = [8, 13]

    is_first_time = False
    skip_make_ids = False
    skip_scraping = False
    these_headwords_only = []

    langcode = "pol"

    """
    Step 1: scrape_word_data()
                        output_words_99_scraped CREATED (ignore unless next fxn encounters error)
                        rejected_words_99 CREATED
                generate_adjective()/minimise_verbs()
                        output_words_99 CREATED
                        truncated_words_99 CREATED

    Step 1.5: Whittle translations and manually add shorthand tags in truncated_words_99. Move all files to output_saved.
                        truncated_words_99 MODIFIED

    Step 2: finalise_lemma_objects()
                untruncate_lemma_objects()
                        untruncated_words_99 CREATED
                expand_tags_and_topics()
                        finished_words_99 CREATED             
    """

    head_words_ref = {
        "adjectives": adjectives,
        "nouns": nouns,
        "verbs": verbs
    }
    lang_ref = {
        "pol": "Polish"
    }

    head_words = these_headwords_only if these_headwords_only \
        else head_words_ref[wordtype][input_indexes[0]:input_indexes[1]]

    if step == 1:
        scrape_word_data(
            group_number=group_number,
            head_words=head_words,
            wordtype=wordtype,
            language=lang_ref[langcode],
            skip_scraping=skip_scraping
        )
    elif step == 2:
        finalise_lemma_objects(group_number, wordtype, langcode, skip_make_ids, is_first_time)