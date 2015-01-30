
"""
    Basic Pastebin scraper that hits the public archives and identifies anything that looks like a password
    Main file.

"""


from scraper.scraper import PageScraper, PWID


if __name__ == "__main__":

    pwid = PWID()

    password_matches = []

    scraper = PageScraper("http://pastebin.com")
    scraper.scrape("http://pastebin.com/archive")
    table_links = scraper.find('//table[@class="maintable"]//a/@href')
    links = scraper.parse_table_links(table_links)

    page_scraper = PageScraper("http://pastebin.com")

    for link in links:
        page_scraper.scrape(link)
        text = page_scraper.find('//textarea[@class="paste_code"]/text()')

        possible_passwords = None
        if text:
            possible_passwords = pwid.identify_passwords(text[0])

        if possible_passwords:
            password_matches.append((link, possible_passwords))

    for pwm in password_matches:
        print pwm


