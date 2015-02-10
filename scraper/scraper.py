
"""
    Basic Pastebin scraper that hits the public archives and identifies anything that looks like a password

"""

import re
import requests
from lxml import html

from filter import TextFilter


class PWID(object):
    """
    Finds passwords that are characters and digits, and are at least 8 characters long.
    Basic regex also includes special characters except spaces.
    """

    PW_MIN_LENGTH = 8
    PW_MAX_LENGTH = 48

    filter = None

    def __init__(self):
        self.re_pattern = re.compile('(\w+\d+[\w\d\S]+)|(\d+\w+[\w\d\S]+)')
        self.filter = TextFilter()

    def identify_passwords(self, str_input):
        matches = self.re_pattern.findall(str_input)

        prepared_matches = []

        for match in matches:
            for item in match:

                passed_filtering = self.filter.apply_filter(item)
                valid_length = self.PW_MIN_LENGTH <= len(item) <= self.PW_MAX_LENGTH

                if item and valid_length and passed_filtering:
                    prepared_matches.append(item)

        return prepared_matches




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

    def find(self, pattern ):
        result = self.page_tree.xpath(pattern)
        return result

    def parse_table_links(self, links):

        results = []

        for link in links:
            # remove the archive links and only take the links to public pastes
            if not str(link).startswith('/archive'):
                results.append('{}{}'.format(self.target_url, link))

        return results
