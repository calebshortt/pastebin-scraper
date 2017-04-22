
"""
    Basic Pastebin scraper that hits the public archives and identifies anything that looks like a password

    Main file.

"""


from presets.pastebin import PastebinScraper


if __name__ == "__main__":

    print('Executing...')

    pastebin_scraper = PastebinScraper(fast=False, ultra_verbose=True)
    password_matches = pastebin_scraper.analyze()

    print('Done.\nPotential Passwords:')

    for pwm in password_matches:
        print pwm


