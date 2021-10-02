from parser_classes.Polish_parsers import PolishNounHTMLParser
from scraper_utils.common import scrape_word_data
from input.Polish.input_words import nouns_1

if __name__ == '__main__':
    num = 1
    input_words = nouns_1[0:2]

    print(f'# Starting, given {len(input_words)} words.')

    num = str(num)[-2:].zfill(2)
    output_path = f"output_nouns_{num}"
    rejected_path = f"rejected_nouns_{num}"

    scrape_word_data(
        "Polish",
        PolishNounHTMLParser(convert_charrefs=False),
        input_words,
        use_sample=False,
        output_file=output_path,
        rejected_file=rejected_path
    )

    print(f"\n# Finished scraping for {len(input_words)} words:", input_words)