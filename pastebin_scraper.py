
"""
    Basic Pastebin scraper that hits the public archives and identifies anything that looks like a password

    Main file.

"""

import time

from presets.pastebin import PastebinScraper


if __name__ == "__main__":

    # print('Executing...')

    max_iterations = 100
    curr_iteration = 0
    wait_time_s = 300   # 5 minutes (300s)
    main_start_time = time.time()

    while curr_iteration < max_iterations:

        cur_start_time = time.time()
        print('Executing Iteration %s of %s...' % (curr_iteration, max_iterations))

        pastebin_scraper = PastebinScraper(fast=False, ultra_verbose=True, save_filtered=True)
        password_matches = pastebin_scraper.analyze()

        print('Potential Passwords:')

        for pwm in password_matches:
            print pwm

        print('Execution Time: %s seconds.' % (time.time() - cur_start_time))
        print('Waiting %s seconds...' % wait_time_s)
        time.sleep(wait_time_s)
        curr_iteration += 1

    print('Total System Execution Time: %s seconds' % (time.time() - main_start_time))


