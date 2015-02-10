
from setuptools import setup, find_packages

__version__ = '1.0.2'

setup(
    name='PBPWScraper',
    version=__version__,
    description='A simple scraper of the public posts on pastebin. It looks for passwords.',
    author='Caleb Shortt',
    author_email='caleb@rgauge.com',
    url='https://bitbucket.org/cshortt/pastebin-scraper/',
    packages=find_packages(),
    keywords=[
        'pastebin',
        'scraper'
        'python',
        'password',
    ],
    install_requires=[
        'lxml==3.4.1',
        'requests==2.5.1',
        'wsgiref==0.1.2',
    ], 
)

