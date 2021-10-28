from parsers.Polish_adjective_parser import *
from parsers.Polish_noun_parser import *
from parsers.Polish_verb_parser import *
from scraper_utils.processing import *
from input.Polish.nouns.head_words import input as nouns
from input.Polish.adjectives.head_words import input as adjectives
from input.Polish.verbs.head_words import input as verbs
from semimanual_utils.Polish import *


if __name__ == '__main__':
    wordtypecode = "v"
    group_number = 333
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

    if wordtypecode[0] == "a":
        wordtype = "adjectives"
        parser = PolishAdjectiveParser(convert_charrefs=False)
        head_words = adjectives[input_indexes[0]:input_indexes[1]]
    elif wordtypecode[0] == "n":
        wordtype = "nouns"
        parser = PolishNounParser(convert_charrefs=False)
        head_words = nouns[input_indexes[0]:input_indexes[1]]
    elif wordtypecode[0] == "v":
        wordtype = "verbs"
        parser = PolishVerbParser(convert_charrefs=False)
        head_words = verbs[input_indexes[0]:input_indexes[1]]
    else:
        raise Exception(f'Expected wordtypecode to be one of ["a","n","v"]')

    if step == 1:
        scrape_word_data(
            group_number=group_number,
            head_words=head_words,
            wordtype=wordtype,
            parser=parser,
            language="Polish",
            scraping_already_done=scraping_already_done
        )
    elif step == 3:
        finalise_lemma_objects(group_number, wordtype)