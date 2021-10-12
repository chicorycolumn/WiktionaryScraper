from parsers.Polish_adjective_parser import *
from scraper_utils.processing import *
from input.Polish.nouns.head_words import input as nouns
from input.Polish.adjectives.head_words import input as adjectives
from semimanual_utils.Polish import *

""""
Step 1: scrape_word_data()
                    output_nouns_99 CREATED
                    truncated_nouns_99 CREATED
                    rejected_nouns_99 CREATED

Step 2: Manually add shorthand tags
                    truncated_nouns_99 MODIFIED

Step 3: untruncate_lemma_objects([99])
                    untruncated_nouns_99 CREATED

Step 4: fill_out_lemma_objects([99], wordtype)
                    finished_nouns_99 CREATED
"""

def get_adjectives():
    wordtype = "adjectives"

    scrape_word_data(
        group_number=2,
        head_words=["niebieski"],
        wordtype=wordtype,

        parser=PolishAdjectiveParser(convert_charrefs=False),
        language="Polish",
        use_sample=True,
    )

    # res_arr = [generate_adjective(args_set) for args_set in scraped_args_sets]


def get_nouns():
    wordtype = "nouns"

    # Group 1 = words 00 -  50
    # Group 2 = words 50 - 100
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