
import re
import logging


FORMAT = '%(asctime)-15s [Filter] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TextFilter(object):

    fast = False

    def __init__(self, **kwargs):
        self.fast = kwargs.get('fast', self.fast)

    SCORE_THREASHOLD = 0

    aggregate_score = 0

    # Basic dictionary of key phrases and their associated values
    key_phrases = {

        # Common password dump indicators
        'password': 1000,
        'login': 1000,
        'user': 100,
        'username': 100,
        'auth_pass': 1000,
        'auth': 50,
        'dump': 50,
        'hack': 50,
        'crack': 50,
        'netstat': 50,
        'accounts': 50,
        'nmap': 50,
        'wget': 50,


        # File extensions
        '.html': -100,
        '.mov': -100,
        '.htm': -100,
        '.png': -100,
        '.m3u8': -100,
        '.zip': -100,
        '.jar': -100,
        '.php': -100,
        '.jpeg': -100,
        '.jpg': -100,
        '.inc': -100,
        '.mp4': -100,
        '.avi': -100,
        '.mkv': -100,
        '.gif': -100,
        '.java': -100,
        '.py': -100,
        '.csv': -100,
        '.vim': -100,
        '.ts': -100,
        '.app': -100,
        '.c': -100,
        '.txt': -100,
        '.wav': -100,
        '.mp3': -100,
        '.pb': -100,
        '.dmg': -100,
        '.pak': -100,
        '.dll': -100,


        # Domains
        '.net': -50,
        '.com': -50,
        '.co': -50,
        '.uk': -50,
        '.ca': -50,
        '.de': -50,
        '.ru': -50,
        '.onion': -50,
        '.org': -50,


        # Code Filters
        'int': -50,
        'float': -50,
        'decimal': -50,
        'char': -50,
        'string': -50,
        '#include': -50,
        'exception': -100,
        'struct': -50,
        'namespace': -50,
        'class': -50,
        'void': -50,
        '>=': -50,
        '<=': -50,
        'cout': -50,
        '<<': -50,
        '>>': -50,
        'null': -50,
        'for(': -50,
        'while(': -50,
        '){': -50,
        ') {': -50,
        'if(': -50,
        'else(': -50,
        'for (': -50,
        'while (': -50,
        'if (': -50,
        'else (': -50,
        '++': -50,
        ');': -50,
        '==': -50,
        'i=0;': -50,
        'j=0;': -50,
        '()': -50,
        '.Value': -50,
        'jenkins': -50,
        'unstable': -50,
        'unknown': -50,
        'Unknown': -50,
        'resources': -50,
        'image': -50,
        'driver': -50,
        'Direct3D': -50,
        'func': -50,
        'invoke': -50,
        'Native': -50,
        'u32(': -50,
        'pointer': -50,
        '.length': -50,
        '(this': -50,
        '(self': -50,
        '\\n': -50,
        '\\r': -50,
        '#!/usr/bin/env': -50,
        'Int32': -50,
        'new(': -50,
        'DEBUG': -50,
        'timeStamp': -50,
        ';\n': -50,
        ';\r': -50,
        '#!/bin/bash': -50,
        '/usr/': -50,
        '/var/': -50,
        'bin': -50,
        'system32': -50,
        'windows': -50,
        'lib64': -50,
        'DOCTYPE': -50,
        'public': -50,
        'private': -50,
        'static': -50,

        # protocol filters
        'http:': -50,
        'https:': -50,
        'Content-Encoding:': -50,
        'Keep-Alive:': -50,
        'Content-Type:': -50,
        'Server:': -50,
        'dev:': -50,
        'xmlrpc': -50,
        'proxy': -50,

        # Movie files patterns
        'x264': -50,
        'HDTV': -50,
        '720p': -50,

        # HTML/CSS filters
        'px;': -50,
        'container': -50,
        '.Text': -50,
        ':hover': -50,
        'scroll': -50,
        'text': -50,
        'Button': -50,
        'toggle': -50,
        '<div': -50,
        '<h': -50,
        '<p': -50,
        'W3C//DTD': -50,

        #SQL
        'SELECT': -50,
        'WHERE': -50,
        'FROM': -50,


        # General Negative Phrases
        'Minecraft': -50,
        'C:\Windows\system32': -50,
        '10.0.0.0': -50,
        '127.0.0.1': -50,
        'amd64': -50,
        'x64': -50,
        'objects.': -50,
        'x86_64': -15,
    }

    # Patterns (regular expressions) that, if matched, apply scores to the target.
    patterns = {

        # HTML Tags
        '(<.+?>)': -50,

        # Basic hash values, eg: 0x196e17d4
        '(0x[\da-fa-f]{2,8})': -50,

        # Simple IPv4 pattern
        '([\d]{2,3})\.([\d]{2,3})\.([\d]{2,3})\.([\d]{2,3})(:\d{2,4})?': -50,

        # Date / Time Stamps
        # Test Strings:
        # 6:08
        # 12-12-12
        # 12-12-1234
        # 1:22:34
        # 07-12-12 12:34:00
        # 05-Mar-17
        '((\d{1,2}|\d{4})[:-]\d{1,2}[:-](\d{4}|\d{1,2}))': -50,
        '(\d{1,4})+[:\-. \/]?([\d\w]{1,4})[:\-. \/](\d{1,4})': -50,

        # possible entry in password dump:  <user>[: |]<password>
        '^([\w.`~!@#$%&*_-]{0,30})[: |-]+([\w\.\`\~\!\@\#\$\%\&\*\_\-\^\*]{4,32})([ ]+)?$': 100,

        # possible email address password dump
        '^([\w\.\+\-]+@[\w\.\+\-]+\.[\w]{1,10})[: |-]+([\w\.\`\~\!\@\#\$\%\&\*\_\-\^\*]{4,32})([ ]+)?$': 100,


        # code variable assignment
        # Test String:
        # $items = $quoteObj->getAllItems();
        # int test = 10;
        # var test = 1234235;
        # var test = "test"
        # test = 'test'
        # yb=50;
        # String test = 'test'; // this is an inline comment
        # x1=e.offsetX;
        # int[] things = {4,6,78,12,34};
        '([\w\d\$\-\>\<\(\)\[\]\{\}]*[ \t]?)([\w\d\$\-\>\<\(\)\[\]\{\}]*)[ \t]?=[ \t]?([\.\w\d\$\-\>\<\(\)\"\'\[\]\{\}\,]+)[\;]?[ ]*[\n\r]?': -50,

        # Basic base url identifier
        '(http[s]?://)(www.)?([\w\d\-\_\+]+)\.([\w\d]+)([\:]?\d*)[/]?': -50,

    }

    def apply_filter(self, text):

        text_score = 0
        text = text.lower()

        for key_word, score in self.key_phrases.items():
            logger.debug('Applying filter on keyword: %s' % key_word)
            key_word = key_word.lower()
            if key_word in text:
                logger.debug('Success! Keyword is in text.')
                occurrences = [m.start() for m in re.finditer(re.escape(key_word), text)]
                text_score += len(occurrences)*score

        # If fast is set, skip pattern matching
        if not self.fast:

            logger.debug('Using advanced (slower) patterns... (fast = false)')

            for pattern, score in self.patterns.items():

                logger.debug('Checking pattern: %s' % pattern)

                re_pattern = re.compile(pattern, re.MULTILINE)
                matches = re_pattern.findall(text)

                if matches:
                    logger.debug('Success! Pattern is in text.')
                    # only apply the match to the specific pattern once
                    text_score += len(matches)*score

        self.aggregate_score += text_score

        return text_score >= self.SCORE_THREASHOLD









