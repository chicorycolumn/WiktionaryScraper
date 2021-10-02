from parser_classes.Polish_parsers import PolishNounHTMLParser
from scraper_utils.common import scrape_word_data
from input.Polish.input_words import nouns_1

if __name__ == '__main__':
    group_of_input_words = 1
    input_words = nouns_1[0:5] # After adding words input folder, import, then select here how many want scrape.
    # input_words = ["bałagan", "małpa", "schody", "ser", "złodziej"]
    use_sample = False

    print(f'## Starting, given {len(input_words)} words.')

    group_of_input_words = str(group_of_input_words)[-2:].zfill(2)
    output_path = f"output_nouns_{group_of_input_words}"
    rejected_path = f"rejected_nouns_{group_of_input_words}"

    scrape_word_data(
        PolishNounHTMLParser(convert_charrefs=False),
        "Polish",
        input_words,
        use_sample=use_sample,
        output_file=output_path,
        rejected_file=rejected_path,
        group_number=group_of_input_words
    )

    print(f"\n## Finished scraping for {len(input_words)} words:", input_words)