from parsers.Polish_adjective_parser import *
from parsers.Polish_noun_parser import *
from parsers.Polish_verb_parser import *
from scraper_utils.processing import *
from input.Polish.nouns.head_words import input as nouns
from input.Polish.adjectives.head_words import input as adjectives
from input.Polish.verbs.head_words import input as verbs
from semimanual_utils.Polish import *


current_wordtype = "a"


def get_verbs():
    wordtype = "verbs"
    if current_wordtype != wordtype[0]:
        return

    """
    Step 1: scrape_word_data()
                        output_verbs_99 CREATED
                        rejected_verbs_99 CREATED

    Step 2: Move to output_saved; manually add shorthand tags; format translations.
                        output_verbs_99 MODIFIED

    Step 3: generate_verbs([99])
                        finished_verbs_99 CREATED
    """

    scrape_word_data(
        group_number=101,
        head_words=verbs[0:5],
        wordtype=wordtype,
        parser=PolishVerbParser(convert_charrefs=False),
        language="Polish",
        use_sample=False,
    )

    generate_verbs([101], wordtype)


def get_adjectives():
    wordtype = "adjectives"
    if current_wordtype != wordtype[0]:
        return

    """
    Step 1: scrape_word_data()
                        output_protoadjectives_99 CREATED (only useful is generate_adjectives had error)
                        rejected_protoadjectives_99 CREATED
                generate_adjectives([99])
                        output_adjectives_99 CREATED
                        truncated_adjectives_99 CREATED
                        
    Step 2: Move the three files to output_saved; manually add shorthand tags; whittle translations.
                        truncated_adjectives_99 MODIFIED
                    
    Step 3: finalise_lemma_objects([99])
                untruncate_lemma_objects([99])
                        untruncated_adjectives_99 CREATED
                expand_tags_and_topics([99], wordtype)
                        finished_adjectives_99 CREATED
                        
    """

    group_numbers = [222]
    head_words = adjectives[15: 20]
    step = 3

    if step == 1:
        for group_number in group_numbers:
            scrape_word_data(
                group_number=group_number,
                head_words=head_words,
                wordtype=wordtype,
                parser=PolishAdjectiveParser(convert_charrefs=False),
                language="Polish",
                use_sample=False,
            )
    elif step == 3:
        finalise_lemma_objects(group_numbers, wordtype)



def get_nouns():
    wordtype = "nouns"
    if current_wordtype != wordtype[0]:
        return

    """
    Step 1: scrape_word_data()
                        output_nouns_99 CREATED
                        truncated_nouns_99 CREATED
                        rejected_nouns_99 CREATED

    Step 2: Move all three files to output_saved; manually add shorthand tags; whittle translations.
                        truncated_nouns_99 MODIFIED
                    
    Step 3: finalise_lemma_objects([99])
                untruncate_lemma_objects([99])
                        untruncated_nouns_99 CREATED
                expand_tags_and_topics([99], wordtype)
                        finished_nouns_99 CREATED

    # Group 1 = words 00 -  50
    # Group 2 = words 50 - 100
    """

    scrape_word_data(
        group_number=66,
        head_words=nouns[100:105],
        wordtype=wordtype,
        parser=PolishNounParser(convert_charrefs=False),
        language="Polish",
        use_sample=False,
    )

    # finalise_lemma_objects([2], wordtype)


if __name__ == '__main__':
    get_nouns()
    get_adjectives()
    get_verbs()