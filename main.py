from parser_classes.Polish_parsers import PolishNounHTMLParser
from scraper_utils.common import scrape_word_data
from input.Polish.input_words import nouns_1

if __name__ == '__main__':
    group_of_input_words = 1
    input_words = nouns_1[0:2] # After adding words input folder, import, then select here how many want scrape.
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

    print(f'\n## Finished scraping at "{f"output_nouns_{group_of_input_words}"}" for {len(input_words)} words:', input_words)