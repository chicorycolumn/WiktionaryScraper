from input.Polish.nouns.head_words import input as nouns
from input.Polish.adjectives.head_words import input as adjectives
from input.Polish.verbs.head_words import input as verbs
from parsers.common import scrape_word_data
from utils.postprocessing.common import finalise_lemma_objects
from utils.scraping.common import check_rescraped_against_existing
from input.Polish.adjectives.head_words import input

if __name__ == '__main__':

    # check_rescraped_against_existing("adjectives_old", "adjectives_new")
    # for el in input:
    #     if el[-1] not in ["y", "i"]:
    #         print(el)

    step = 1
    group_number = 99
    input_indexes = [0, 870]
    wordtype = "a"
    these_headwords_only = [

    ]
    skip_make_ids = False  # only set True when manually testing.
    skip_scraping = False  # only set True if you've already scraped but want to rerun post-scraping fxns of Step 1.
    reparse_previously_rejected = False  # If you're manually rerunning rejected ones when collecting batch together.
    skip_extras = True  # You know, the extra lemmas to parse gathered from synonyms of lemmas you asked to parse.
    langcode = "pol"

    """

    Step 0  Run this file with step = 0

            This is just to assess which lemmas have been scraped/rejected/yet to scrape.
            No scraping or file writing is done, you just get a printout.


    Step 1  Run this file with step = 1

            scrape_word_data()
                        output_words_99_scraped CREATED (Only useful if following fxn encounters error)
                        rejected_words_99 CREATED

                generate_adjective()/minimise_verbs()
                        output_words_99 CREATED
                        truncated_words_99 CREATED


    Step 1.5 Manual

              (i) *_scraped    Delete it.
                  rejected_*   Move to output_saved/rejected.
                  truncated_*  Move to output_saved.
                  output_*     Move to output_saved.

              (ii) Open truncated_* and whittle translations.

Strings in translations that "(start and end with brackets)" are removed automatically.
Duplicated translations ["wolf", "wolf"] are removed automatically.

              (iii) Manually add shorthand tags (in truncated_*).

Include frequency tag (no comma needed). eg "1v" or "1£,g" or "1b,n,w,t".
Flag lobjs for deletion by adding '!' at start of lemma.
You must duplicate lobjs which have double meaning, and whittle respective translation accordingly, temp_id is adjusted automatically.


    Step 2  Run this file with step = 2 

            finalise_lemma_objects()
                untruncate_lemma_objects()
                        untruncated_words_99 CREATED (This won't have the tags expanded. Look to the other file.)
                expand_tags_and_topics()
                        wordtype_folder/finished_words_99 CREATED

            The finished file is now present in its wordtype folder ie outputsaved/nouns,
            so you can go ahead and delete
             remaining files in output_saved top level.

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

    if not skip_extras and reparse_previously_rejected:
        skip_extras = True

    if step in [0, 1]:
        scrape_word_data(
            group_number=group_number,
            head_words=head_words,
            wordtype=wordtype,
            language=lang_ref[langcode],
            skip_scraping=skip_scraping,
            just_assess_scrape_status_of_lemmas=step == 0,
            reparse_previously_rejected=reparse_previously_rejected,
            skip_extras=skip_extras
        )
    elif step == 2:
        finalise_lemma_objects(group_number, wordtype, langcode, skip_make_ids)
