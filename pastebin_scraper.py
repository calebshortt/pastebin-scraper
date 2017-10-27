
"""
    Basic Pastebin scraper that hits the public archives and identifies anything that looks like a password

    Main file.

"""

import time
import sys
import json
import uuid

from presets.pastebin import PastebinScraper
from settings import ROOT_DIR
from networking.export import CatServerExporter


if __name__ == "__main__":

    # print('Executing...')

    reload(sys)
    sys.setdefaultencoding('utf8')

    max_iterations = 100
    curr_iteration = 0
    wait_time_s = 300   # 5 minutes (300s)
    main_start_time = time.time()

    # already_seen = {}

    pastebin_scraper = PastebinScraper(fast=False, ultra_verbose=True, save_filtered=True)

    filepath = ROOT_DIR + '/formatted_output'
    identifier = uuid.uuid4()

    exporter = CatServerExporter()

    while curr_iteration < max_iterations:

        cur_start_time = time.time()
        print('Executing Iteration %s of %s...' % (curr_iteration, max_iterations))

        # pastebin_scraper = PastebinScraper(fast=False, ultra_verbose=True, save_filtered=True)
        password_matches = pastebin_scraper.analyze()
        pastebin_scraper.clear_passwords()

        print('Potential Passwords:')

        filename = '%s/%s.json' % (filepath, identifier)

        with open(filename, 'a') as f:
            for pwm in password_matches:
                print pwm

                jsn = json.dumps(pwm)
                f.write('%s\n' % jsn)

                exporter.export(pwm)




        print('Execution Time: %s seconds.' % (time.time() - cur_start_time))
        print('Waiting %s seconds...' % wait_time_s)
        time.sleep(wait_time_s)
        curr_iteration += 1

    print('Total System Execution Time: %s seconds' % (time.time() - main_start_time))


