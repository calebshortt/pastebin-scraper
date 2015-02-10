
================
Pastebin Scraper
================


Description
-----------

This project is a simple scraper that targets the website "pastebin". It scans through the public paste archives
and looks for anything that might match a password-like pattern.

It has been designed to be easily extensible for other pages or websites.


Installation
------------

The Pastebin Password Scraper is on pip (https://pip.pypa.io/en/latest/).

This is the easiest way to install the PBPWScraper:

.. code-block:: python

    pip install PBPWScraper


If you do not want to use pip you can clone the repository here.


Usage
-----

An example is in pastebin_scraper.py:

.. code-block:: python

    from presets.pastebin import PastebinScraper

    if __name__ == "__main__":

        pastebin_scraper = PastebinScraper()
        password_matches = pastebin_scraper.analyze()

        for pwm in password_matches:
            print pwm


Requirements
------------

* All requirements are listed in requirements.txt

Install them using pip at https://pip.pypa.io/en/latest/


.. code-block:: python

    pip install -r requirements.txt


* The setup script will install the requirements if pip is installed.







