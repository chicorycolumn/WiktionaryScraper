from unittest import TestCase
from main import PolishNounHTMLParser
from scraper_utils.common import scrape_word_data


class TestPolishNounHTMLParser(TestCase):

    def test_scraper_locally(self):
        with open(f'output/expected_output_polish_1.json', 'r') as f:
            expected = f.read()
            f.close()

        scrape_word_data(
            "Polish",
            PolishNounHTMLParser(convert_charrefs=False),
            ["baba", "bałagan", "cel", "drzwi", "dzień", "małpa", "miesiąc", "rok", "ser"],
            True,
            # ["prysznic", "glista", "gleba", "łeb", "palec", "noga", "piła", "piłka"],
            # False,
            "output_polish_1"
        )

        with open(f'output/output_polish_1.json', 'r') as f:
            actual = f.read()
            f.close()

        assert actual == expected

    def test_scraper_remotely(self):
        with open(f'output/expected_output_polish_2.json', 'r') as f:
            expected = f.read()
            f.close()

        scrape_word_data(
            "Polish",
            PolishNounHTMLParser(convert_charrefs=False),
            ["prysznic", "glista", "gleba", "łeb", "palec", "noga", "piła", "piłka"],
            False,
            "output_polish_1"
        )

        with open(f'output/output_polish_2.json', 'r') as f:
            actual = f.read()
            f.close()

        assert actual == expected

