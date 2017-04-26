
import unittest
import logging
import sys

from utils import load_corpus
from scraper.scraper import PWID


logger = logging.getLogger()
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


class ScraperTest(unittest.TestCase):

    no_passwords = [
        'corpus/negative/ncf01.txt',
        'corpus/negative/ncf02.txt',
        'corpus/negative/ncf03.txt',
        # 'corpus/negative/ncf04.txt',
    ]

    passwords = [
        'corpus/positive/pcf01.txt',
        'corpus/positive/pcf02.txt',
    ]

    anomalies = [
        'corpus/anomalies/anom01.txt',
        'corpus/anomalies/anom02.txt',
        'corpus/anomalies/anom03.txt',
        'corpus/anomalies/anom04.txt',
        'corpus/anomalies/anom05.txt',
    ]

    def test_PWID(self):
        """
        Simply run through a corpus to make sure that it is loaded and analyzed
        :return:
        """

        text = load_corpus(self.passwords[0])
        pwid = PWID(ultra_verbose=True, fast=False)

        matches, score = pwid.identify_passwords(text)

        assert len(matches) > 0

    def test_PWID_passwords(self):

        pwid = PWID(ultra_verbose=True, fast=False)

        for file_path in self.passwords:

            logger.info('Executing on %s' % file_path)

            text = load_corpus(file_path)
            matches, score = pwid.identify_passwords(text)

            print score, matches
            assert score > 0

    def test_PWID_no_passwords(self):

        pwid = PWID(ultra_verbose=True, fast=False)

        for file_path in self.no_passwords:

            logger.info('Executing on %s' % file_path)

            text = load_corpus(file_path)
            matches, score = pwid.identify_passwords(text)

            print score, matches
            assert score <= 0

    def test_PWID_anomalies(self):
        """
        None of the anomalies should register a positive score.
        Anomalies are more likely than other texts to register a positive score from the filters and produce false
        positives.
        :return:
        """

        pwid = PWID(ultra_verbose=True, fast=False)

        for file_path in self.anomalies:

            logger.info('Executing on %s' % file_path)

            text = load_corpus(file_path)
            matches, score = pwid.identify_passwords(text)

            print score, matches
            print pwid.filter.aggregate_score

            assert score <= 0













