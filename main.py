from input.Polish.nouns.head_words import input as nouns
from input.Polish.adjectives.head_words import input as adjectives
from input.Polish.verbs.head_words import input as verbs
from parsers.common import scrape_word_data
from utils.postprocessing.common import make_ids, finalise_lemma_objects

if __name__ == '__main__':

    step = 1
    group_number = 22
    wordtype = "verbs"
    input_indexes = [0, 50]

    skip_make_ids = False
    skip_scraping = False # set True if you've already scraped but want to rerun post-scraping fxns of Step 1.
    these_headwords_only = []

    langcode = "pol"

    """
    Step 1: scrape_word_data()
                        output_words_99_scraped CREATED (delete unless next fxn encounters error)
                        rejected_words_99 CREATED
                generate_adjective()/minimise_verbs()
                        output_words_99 CREATED
                        truncated_words_99 CREATED

    Step 1.5: Take truncated_words_99 and whittle translations 
(Don't worry about strings in the translations array that start and end with brackets, they will be removed automatically.)
(Don't worry about duplicated translations eg ["wolf", "wolf"] as these will be removed automatically.)
              Manually add shorthand tags. 
(Make sure include frequency tag, but no comma needed. eg "v1" or "!,g1" or "b,n,w,t1".)
              Flag lobjs for deletion simply by adding '!' at start of lemma.
              Move all files to output_saved.
                        truncated_words_99 MODIFIED

    Step 2: finalise_lemma_objects()
                untruncate_lemma_objects()
                        untruncated_words_99 CREATED (Remember, this won't have the tags expanded. Look to the other file.)
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

    head_words = list({el for el in head_words})

    if step == 1:
        scrape_word_data(
            group_number=group_number,
            head_words=head_words,
            wordtype=wordtype,
            language=lang_ref[langcode],
            skip_scraping=skip_scraping
        )
    elif step == 2:
        finalise_lemma_objects(group_number, wordtype, langcode, skip_make_ids)