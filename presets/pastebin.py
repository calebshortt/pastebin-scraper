
import logging
import time

from scraper.scraper import PageScraper, PWID


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.WARNING)
log = logging.getLogger(__name__)


class PastebinScraper(object):

    pw_identifier = None
    scraper = None

    crawler_delay = .5

    password_matches = []
    base_url = 'http://pastebin.com'
    scraper_target_url = 'http://pastebin.com/archive'

    fast = False

    def __init__(self, **kwargs):

        self.base_url = kwargs.get('base_url', self.base_url)
        self.fast = kwargs.get('fast', self.fast)
        self.scraper = PageScraper(url=self.base_url, scrape=False)
        self.pw_identifier = PWID(fast=self.fast)

    def analyze(self):

        log.info("Scraping target: %s..." % self.scraper_target_url)
        self.scraper.scrape(self.scraper_target_url)
        log.info("Finding links...")
        table_links = self.scraper.find('//table[@class="maintable"]//a/@href')
        links = self.scraper.parse_table_links(table_links)

        page_scraper = PageScraper("http://www.pastebin.com", scrape=False)
        # page_scraper = PageScraper(None)

        log.info("Links Found: %s" % len(links))

        for link in links:

            log.info('Analyzing Link: {}'.format(link))

            page_scraper.scrape(link)
            log.debug("Finding paste text area")
            text = page_scraper.find('//textarea[@class="paste_code"]/text()')

            possible_passwords = None
            if text:
                log.debug("Running password identifier...")
                possible_passwords = self.pw_identifier.identify_passwords(text[0])
                log.debug("Done")

            if possible_passwords:
                self.password_matches.append((link, possible_passwords))

            time.sleep(self.crawler_delay)

        return self.password_matches











