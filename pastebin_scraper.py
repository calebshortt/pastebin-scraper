
"""
    Basic Pastebin scraper that hits the public archives and identifies anything that looks like a password

    Main file.

"""


from presets.pastebin import PastebinScraper


if __name__ == "__main__":

    pastebin_scraper = PastebinScraper()
    password_matches = pastebin_scraper.analyze()

    for pwm in password_matches:
        print pwm


