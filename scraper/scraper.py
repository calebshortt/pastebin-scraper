
"""
    Basic Pastebin scraper that hits the public archives and identifies anything that looks like a password

"""

import re
import requests
from lxml import html

from filter import TextFilter
from frequency_analysis import PWAnalyzer


class PWID(object):
    """
    Finds passwords that are characters and digits, and are at least 8 characters long.
    Basic regex also includes special characters except spaces.
    Searches a resource file of common passwords and adds any string that contains them.
    """

    PW_MIN_LENGTH = 8
    PW_MAX_LENGTH = 48

    filter = None

    passwords = []

    def __init__(self):
        # self.re_pattern = re.compile('(\w+\d+[\w\d\S]+)|(\d+\w+[\w\d\S]+)')
        self.filter = TextFilter()
        self.freq_analyzer = PWAnalyzer()

        self.passwords = self._load_resources()

        try:
            self.freq_analyzer.import_resource()
        except Exception:
            pass

    def identify_passwords(self, str_input):
        """
        Given the string input, try to identify anything that looks like a password or identifier of interest.

        :param str_input:
        :return:
        """
        matches = self.filter_matches(str_input)

        prepared_matches = []
        match_confidence = 0

        for item in matches:
            # for item in match:

            text_score = self.filter.apply_filter(item)
            match_confidence += text_score
            passed_filtering = text_score >= TextFilter.SCORE_THREASHOLD

            valid_length = self.PW_MIN_LENGTH <= len(item) <= self.PW_MAX_LENGTH

            if item and valid_length and passed_filtering:

                # Add a weighted value of the text based on what characters are in it
                match_confidence += self.freq_analyzer.calculate_weighted_value(item, TextFilter.PASSWORD_DISCOVERY)

                prepared_matches.append(item)

            for password in self.passwords:
                if password in item and item not in prepared_matches:
                    match_confidence += TextFilter.PASSWORD_DISCOVERY
                    prepared_matches.append(item)

        return prepared_matches, match_confidence

    def filter_matches(self, str_input):

        re_pattern = re.compile('[\w\S]{8,48}')
        matches = re_pattern.findall(str_input)

        filtered_matches = []

        for match in matches:
            cap_matches = re.search('[A-Z]+', match)
            low_matches = re.search('[a-z]+', match)
            dig_matches = re.search('\d+', match)

            if cap_matches and low_matches and dig_matches:
                filtered_matches.append(match)

        return filtered_matches

    def _load_resources(self, path='resources/passwords.txt'):
        """
        Opens a given resource and attempts to parse the data.
        Assumes the file is formatted with a single entry per line.
        Adds the results to the password frequency analysis library.

        :param path:
        :return: list of entries
        """
        with open(path) as f:
            content = f.readlines()

        lines = [line.strip() for line in content]

        self.freq_analyzer.import_resource(path)

        return lines


class PageScraper(object):
    """
    Provides a few tools to scrape a page and handle the resulting output.
    """

    page_tree = None
    target_url = None

    def __init__(self, url):
        if url:
            self.page_tree = self.scrape(url)
            self.target_url = url

    def scrape(self, url):
        page = requests.get(url)
        self.page_tree = html.fromstring(page.text)
        return self.page_tree

    def find(self, pattern):
        result = self.page_tree.xpath(pattern)
        return result

    def parse_table_links(self, links):

        results = []

        for link in links:
            # remove the archive links and only take the links to public pastes
            if not str(link).startswith('/archive'):
                results.append('{}{}'.format(self.target_url, link))

        return results
