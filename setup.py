
from setuptools import setup, find_packages
from pip.req import parse_requirements


# Grab the requirements using pip
install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]


__version__ = '1.0.1'

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
    install_requires=reqs,
)

