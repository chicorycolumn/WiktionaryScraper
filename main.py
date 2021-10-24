from parsers.Polish_adjective_parser import *
from parsers.Polish_noun_parser import *
from parsers.Polish_verb_parser import *
from scraper_utils.processing import *
from input.Polish.nouns.head_words import input as nouns
from input.Polish.adjectives.head_words import input as adjectives
from input.Polish.verbs.head_words import input as verbs
from semimanual_utils.Polish import *


def get_verbs():
    wordtype = "verbs"

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

    """
    Step 1: scrape_word_data()
                        output_adjectives_99 CREATED
                        rejected_adjectives_99 CREATED

    Step 2: Move to output_saved; manually add shorthand tags; whittle translations.
                        output_adjectives_99 MODIFIED

    Step 3: generate_adjectives([99])
                        finished_adjectives_99 CREATED
    """

    scrape_word_data(
        group_number=101,
        head_words=adjectives[0:5],
        wordtype=wordtype,
        parser=PolishAdjectiveParser(convert_charrefs=False),
        language="Polish",
        use_sample=False,
    )

    generate_adjectives([101], wordtype)


def get_nouns():
    wordtype = "nouns"

    """
    Step 1: scrape_word_data()
                        output_nouns_99 CREATED
                        truncated_nouns_99 CREATED
                        rejected_nouns_99 CREATED

    Step 2: Move to output_saved; manually add shorthand tags; whittle translations.
                        truncated_nouns_99 MODIFIED

    Step 3: untruncate_lemma_objects([99])
                        untruncated_nouns_99 CREATED

    Step 4: fill_out_lemma_objects([99], wordtype)
                        finished_nouns_99 CREATED

    # Group 1 = words 00 -  50
    # Group 2 = words 50 - 100
    """

    scrape_word_data(
        group_number=2,
        head_words=nouns[50:100],
        wordtype=wordtype,
        parser=PolishNounParser(convert_charrefs=False),
        language="Polish",
        use_sample=False,
    )

    untruncate_lemma_objects([1, 2], wordtype)

    fill_out_lemma_objects([1], wordtype)


if __name__ == '__main__':
    # get_nouns()
    get_adjectives()