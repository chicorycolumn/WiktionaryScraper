from parser_classes.Polish_parsers import PolishNounHTMLParser
from scraper_utils.processing import *
from input.Polish.input_words import nouns_1

""""
Step One: Run scrape_word_data.
    output_nouns_99 CREATED
    truncated_nouns_99 CREATED
    rejected_nouns_99 CREATED

Step Two: Manually add shorthand tags
    truncated_nouns_99 MODIFIED

Step Three: Run untruncate_lemma_objects([99]).
    untruncated_nouns_99 CREATED

Step Four: Run fill_out_lemma_objects([99], wordtype).
    finished_nouns_99 CREATED
"""

if __name__ == '__main__':

    # Group 1 = words 00 -  50
    # Group 2 = words 50 - 100
    scrape_word_data(
        group_number=2,
        head_words=nouns_1[50:100],  # After adding words input folder, import, then select here how many want scrape.
        # # # # # # # # # #
        parser=PolishNounHTMLParser(convert_charrefs=False),
        language="Polish",
        use_sample=False,
    )

    # untruncate_lemma_objects([1, 2])

    # fill_out_lemma_objects([1], "noun")

