
"""
    Basic Pastebin scraper that hits the public archives and identifies anything that looks like a password

"""

import logging
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
    fast = False

    generic_pw_pattern = '(\w+\d+[\w\d\S]+)|(\d+\w+[\w\d\S]+)'
    # generic_pw_pattern = '([\w\d\S\$]{0,32})'

    def __init__(self, **kwargs):
        self.fast = kwargs.get('fast', self.fast)
        self.re_pattern = re.compile(self.generic_pw_pattern)
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

        logging.info("Filter Score: {}".format(self.filter.aggregate_score))

        score_length_ratio = float(self.filter.aggregate_score)/len(str_input)
        logging.info("Score-Length Ratio: {}".format(score_length_ratio))

        self.filter.aggregate_score = 0

        return prepared_matches


class PageScraper(object):
    """
    Provides a few tools to scrape a page and handle the resulting output.
    """

    page_tree = None
    target_url = None

    def __init__(self, url=None):
        if url:
            self.page_tree = self.scrape(url)
            self.target_url = url

    def scrape(self, url):
        u_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        al = 'en-US,en;q=0.8'
        ae = 'gzip, deflate, sdch'
        cc = 'max-age=0'
        conn = 'keep-alive'
        h = 'pastebin.com'

        headers = {
            'User-Agent': u_agent,
            'Accept': accept,
            'Accept-Language': al,
            'Accept-Encoding': ae,
            'Cache-Control': cc,
            'Connection': conn,
            'Host': h
        }

        sess = requests.session()
        page = sess.get(url, headers=headers)

        # page = requests.get(url, headers=headers)
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
