from input.Polish.nouns.head_words import input as nouns
from input.Polish.adjectives.head_words import input as adjectives
from input.Polish.verbs.head_words import input as verbs
from parsers.common import scrape_word_data
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing

if __name__ == '__main__':

    # check_rescraped_against_existing("adjectives_old", "adjectives_new")

    step = 2
    group_number = 2
    input_indexes = [0, 200]
    wordtype = "a"
    these_headwords_only = []
    # these_headwords_only = ['lekki']
    skip_make_ids = False  # only set True when manually testing.
    skip_scraping = False  # only set True if you've already scraped but want to rerun post-scraping fxns of Step 1.
    langcode = "pol"

    """
    
    Step 1  Run this file with step = 1
            
            scrape_word_data()
                        output_words_99_scraped CREATED (Only useful if following fxn encounters error)
                        rejected_words_99 CREATED
            
                generate_adjective()/minimise_verbs()
                        output_words_99 CREATED
                        truncated_words_99 CREATED
                        

    Step 1.5 Manual
    
              (i) Delete *_scraped then move all three files to output_saved.
    
              (ii) Take truncated_*s_99 and whittle translations
    
Don't worry about strings in the translations array that start and end with brackets, they will be removed automatically.
Don't worry about duplicated translations eg ["wolf", "wolf"] as these will be removed automatically.
              
              (iii) Manually add shorthand tags. 

Make sure include frequency tag, but no comma needed. eg "v1" or "!,g1" or "b,n,w,t1".
Flag lobjs for deletion simply by adding '!' at start of lemma.
              
                        truncated_words_99 MODIFIED


    Step 2  Run this file with step = 2 
    
            finalise_lemma_objects()
                untruncate_lemma_objects()
                        untruncated_words_99 CREATED (This won't have the tags expanded. Look to the other file.)
                expand_tags_and_topics()
                        wordtype_folder/finished_words_99 CREATED
                        
    """
    wordtypes = ["nouns", "verbs", "adjectives"]
    for w in wordtypes:
        if wordtype[0] == w[0] or wordtype[0:3] == w[0:3] or wordtype == w:
            wordtype = w

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
