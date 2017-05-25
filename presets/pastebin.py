
import logging
import time
import uuid
import json
import hashlib

from scraper.scraper import PageScraper, PWID
from settings import ROOT_DIR
from categorization.text_parsing import Digestor, CONSTANTS


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.WARNING)
log = logging.getLogger(__name__)


class PastebinScraper(object):

    pw_identifier = None
    scraper = None
    digestor = None

    crawler_delay = .5

    password_matches = []
    base_url = 'http://pastebin.com'
    scraper_target_url = 'http://pastebin.com/archive'

    fast = False
    ultra_verbose = True
    save_filtered = False

    text_save_path = ""
    metrics_save_path = ""

    already_hashed = {}

    def __init__(self, **kwargs):
        """

        :param kwargs:
            base_url:
                (string) The base url of the site to scrape. Default is 'http://pastebin.com'.

            fast:
                (boolean) execute a fast scrape -- will not run pattern filters (which are slower).
                Will only run a keyword search on the text. Default is False.

            save_filtered:
                (boolean) If a text passes the filters with a score greater than 0, save the text to file.
                Default is False.

        :return:
        """

        self.text_save_path = ROOT_DIR + '/filter_saves'
        self.metrics_save_path = ROOT_DIR + '/metric_saves'

        self.base_url = kwargs.get('base_url', self.base_url)
        self.fast = kwargs.get('fast', self.fast)
        self.ultra_verbose = kwargs.get('ultra_verbose', self.ultra_verbose)
        self.save_filtered = kwargs.get('save_filtered', self.save_filtered)
        self.scraper = PageScraper(url=self.base_url, scrape=False)
        self.pw_identifier = PWID(fast=self.fast, ultra_verbose=self.ultra_verbose)
        self.digestor = Digestor()

    def analyze(self):

        log.info("Scraping target: %s..." % self.scraper_target_url)
        self.scraper.scrape(self.scraper_target_url)
        log.info("Finding links...")
        table_links = self.scraper.find('//table[@class="maintable"]//a/@href')
        links = self.scraper.parse_table_links(table_links)

        page_scraper = PageScraper("http://www.pastebin.com", scrape=False)

        log.info("Links Found: %s" % len(links))

        for link in links:

            t_hash = hashlib.sha256()
            t_hash.update(link)
            link_digest = t_hash.hexdigest()

            if link_digest in self.already_hashed:
                continue
            else:
                self.already_hashed[link] = True

            log.info('Analyzing Link: {}'.format(link))

            page_scraper.scrape(link)
            log.debug("Finding paste text area")
            text = page_scraper.find('//textarea[@class="paste_code"]/text()')

            possible_passwords = None
            score = 0
            digestor_analytics = None
            formatted_text = ''
            if text:
                u_text = text[0].encode('utf-8')

                t_hash = hashlib.sha256()
                t_hash.update(u_text)
                text_digest = t_hash.hexdigest()

                # if text_digest not in self.already_hashed:
                if text_digest in self.already_hashed:
                    continue

                log.debug("Running password identifier...")
                possible_passwords, score = self.pw_identifier.identify_passwords(u_text)
                log.debug("Done")

                digestor_analytics = self.digestor.digest(u_text)

                self.already_hashed[text_digest] = digestor_analytics

                # --

                heading = '%s\n\n' % json.dumps(digestor_analytics, ensure_ascii=False)
                heading += '='*40
                heading += '\n\n'

                unicode(heading, 'utf-8')

                formatted_text = unicode(heading + u_text)

            if possible_passwords:
                self.password_matches.append((link, score, possible_passwords, digestor_analytics))

            if score > 0 and self.save_filtered:
                self._save_text(formatted_text)

            time.sleep(self.crawler_delay)

        self._save_metrics(self.password_matches)
        return self.password_matches

    def _save_text(self, text):
        file_path = '%s/%s.txt' % (self.text_save_path, uuid.uuid4())

        try:
            with open(file_path, 'w+') as f:
                f.write(text)
        except IOError:
            log.error('Could not write text to file %s' % file_path)

    def _save_metrics(self, metrics_list):
        file_path = '%s/%s.txt' % (self.metrics_save_path, uuid.uuid4())

        try:
            with open(file_path, 'w+') as f:
                for metric in metrics_list:
                    f.write('%s\n' % json.dumps(metric))
        except IOError:
            log.error('Could not write metric to file %s' % file_path)













