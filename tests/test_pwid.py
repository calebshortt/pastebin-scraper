
import unittest

from utils import load_corpus
from scraper.scraper import PWID


class ScraperTest(unittest.TestCase):

    no_passwords = [
        'corpus/negative/ncf01.txt',
        'corpus/negative/ncf02.txt',
    ]

    passwords = [
        'corpus/positive/pcf01.txt',
        'corpus/positive/pcf02.txt',
    ]

    def test_PWID(self):
        """
        Simply run through a corpus to make sure that it is loaded and analyzed
        :return:
        """

        text = load_corpus(self.passwords[0])
        pwid = PWID()

        matches = pwid.identify_passwords(text)

        assert len(matches) > 0

    def test_PWID_passwords(self):

        pwid = PWID()

        for file_path in self.passwords:
            text = load_corpus(file_path)

            matches = pwid.identify_passwords(text)

            assert len(matches) > 0

    def test_PWID_no_passwords(self):

        pwid = PWID()

        for file_path in self.no_passwords:
            text = load_corpus(file_path)

            matches = pwid.identify_passwords(text)

            print matches
            assert len(matches) == 0










