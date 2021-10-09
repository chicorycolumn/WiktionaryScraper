from parser_classes.Polish_parsers import PolishNounHTMLParser
from scraper_utils.common import scrape_word_data
from input.Polish.input_words import nouns_1

if __name__ == '__main__':
    # Group 1 = words 00 -  50
    # Group 2 = words 50 - 100

    group_of_input_words = 2
    input_words = nouns_1[50:100]  # After adding words input folder, import, then select here how many want scrape.
    use_sample = False

    print(f'## Starting, given {len(input_words)} words.')

    scrape_word_data(
        PolishNounHTMLParser(convert_charrefs=False),
        "Polish",
        input_words,
        use_sample=use_sample,
        filepaths={
            "output": f"output_nouns_{group_of_input_words}",
            "rejected": f"rejected_nouns_{group_of_input_words}",
            "truncated": f"truncated_nouns_{group_of_input_words}",
        },
        group_number=group_of_input_words
    )

    print(f'\n## Scraped at "{f"output_nouns_{group_of_input_words}"}" for {len(input_words)} words:', input_words)
