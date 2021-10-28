from parsers.Polish_adjective_parser import *
from parsers.Polish_noun_parser import *
from parsers.Polish_verb_parser import *
from scraper_utils.processing import *
from input.Polish.nouns.head_words import input as nouns
from input.Polish.adjectives.head_words import input as adjectives
from input.Polish.verbs.head_words import input as verbs
from semimanual_utils.Polish import *


def get_verbs(head_words, group_number, step):
    wordtype = "verbs"

    """
    Step 1: scrape_word_data()
                        rejected_verbs_99 CREATED
                        output_fullverbs_99 CREATED (only useful if minimise_verbs has error)
                    minimise_verbs()
                        output_verbs_99 CREATED
                        truncated_verbs_99 CREATED

    Step 2: Move the three files to output_saved; manually add shorthand tags; format translations.
                        truncated_verbs_99 MODIFIED

    Step 3: finalise_lemma_objects()
                untruncate_lemma_objects()
                        untruncated_verbs_99 CREATED
                expand_tags_and_topics()
                        finished_verbs_99 CREATED
    """

    if step == 1:
        scrape_word_data(
            group_number=group_number,
            head_words=head_words,
            wordtype=wordtype,
            parser=PolishVerbParser(convert_charrefs=False),
            language="Polish",
            use_sample=False,
        )
    elif step == 3:
        finalise_lemma_objects(group_number, wordtype)


def get_adjectives(head_words, group_number, step):
    wordtype = "adjectives"

    """
    Step 1: scrape_word_data()
                        output_protoadjectives_99 CREATED (only useful is generate_adjectives had error)
                        rejected_protoadjectives_99 CREATED
                generate_adjectives()
                        output_adjectives_99 CREATED
                        truncated_adjectives_99 CREATED
                        
    Step 2: Move the three files to output_saved; manually add shorthand tags; whittle translations.
                        truncated_adjectives_99 MODIFIED
                    
    Step 3: finalise_lemma_objects()
                untruncate_lemma_objects()
                        untruncated_adjectives_99 CREATED
                expand_tags_and_topics()
                        finished_adjectives_99 CREATED
                        
    """

    if step == 1:
        scrape_word_data(
            group_number=group_number,
            head_words=head_words,
            wordtype=wordtype,
            parser=PolishAdjectiveParser(convert_charrefs=False),
            language="Polish",
            use_sample=False,
        )
    elif step == 3:
        finalise_lemma_objects(group_number, wordtype)



def get_nouns(head_words, group_number, step):
    wordtype = "nouns"

    """
    Step 1: scrape_word_data()
                        output_nouns_99 CREATED
                        truncated_nouns_99 CREATED
                        rejected_nouns_99 CREATED

    Step 2: Move all three files to output_saved; manually add shorthand tags; whittle translations.
                        truncated_nouns_99 MODIFIED
                    
    Step 3: finalise_lemma_objects()
                untruncate_lemma_objects()
                        untruncated_nouns_99 CREATED
                expand_tags_and_topics()
                        finished_nouns_99 CREATED

    # Group 1 = words 00 -  50
    # Group 2 = words 50 - 100
    """

    if step == 1:
        scrape_word_data(
            group_number=group_number,
            head_words=head_words,
            wordtype=wordtype,
            parser=PolishNounParser(convert_charrefs=False),
            language="Polish",
            use_sample=False,
        )
    elif step == 3:
        finalise_lemma_objects(group_number, wordtype)


if __name__ == '__main__':
    wordtype = "v"
    group_number = 333
    input_indexes = [0,5]
    step = 1

    if wordtype[0] == "a":
        get_adjectives(adjectives[input_indexes[0]:input_indexes[1]], group_number, step)
    elif wordtype[0] == "n":
        get_nouns(nouns[input_indexes[0]:input_indexes[1]], group_number, step)
    elif wordtype[0] == "v":
        get_verbs(verbs[input_indexes[0]:input_indexes[1]], group_number, step)
