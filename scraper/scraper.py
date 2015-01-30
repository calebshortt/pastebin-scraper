
"""
    Basic Pastebin scraper that hits the public archives and identifies anything that looks like a password

"""

import re
import requests
from lxml import html


class PWID(object):

    def __init__(self):
        self.re_pattern = re.compile('(\w+\d+[\w\d\S]+)|(\d+\w+[\w\d\S]+)')

    def identify_passwords(self, str_input):
        matches = self.re_pattern.findall(str_input)

        prepared_matches = []

        for match in matches:
            for item in match:
                if item:
                    prepared_matches.append(item)

        return prepared_matches


class PageScraper(object):

    page_tree = None
    target_url = None

    def __init__(self, url=None):
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
            if not str(link).startswith('/archive'):
                results.append('{}{}'.format(self.target_url, link))

        return results
