
import re
import logging


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
        '.html': -50,
        '.mov': -50,
        '.htm': -50,
        '.png': -50,
        '.m3u8': -50,
        '.zip': -50,
        '.jar': -50,
        '.php': -50,
        '.jpeg': -50,
        '.jpg': -50,
        '.inc': -50,
        '.mp4': -50,
        '.avi': -50,
        '.mkv': -50,
        '.gif': -50,
        '.java': -50,
        '.py': -50,
        '.csv': -50,
        '.vim': -50,
        '.ts': -50,
        '.app': -50,
        '.c': -50,
        '.txt': -50,
        '.wav': -50,
        '.mp3': -50,
        '.pb': -50,
        '.dmg': -50,


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
        '#include': -50,
        'struct': -50,
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
        'jenkins': -50,
        'unstable': -50,
        'unknown': -50,
        'Unknown': -50,
        'func': -50,
        'invoke': -50,
        'Native': -50,
        'u32(': -50,
        'pointer': -50,
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

        # protocol filters
        'http:': -50,
        'Content-Encoding:': -50,
        'Keep-Alive:': -50,
        'Content-Type:': -50,
        'Server:': -50,
        'dev:': -50,
        'xmlrpc': -50,

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

        # Date / Time Stamps
        # Test Strings:
        # 6:08
        # 12-12-12
        # 12-12-1234
        # 1:22:34
        # 07-12-12 12:34:00
        # 05-Mar-17
        '((\d{1,2}|\d{4})[:-]\d{1,2}[:-](\d{4}|\d{1,2}))': -50,
        '(\d{1,4})+[:\-. \/]?([\d\w]{1,4})*[:\-. \/](\d{1,4})+': -50,

        # possible entry in password dump:  <user>[: |]<password>
        '([\w.`~!@#$%&*_-]{0,20})[: |-]([\w.`~!@#$%&*_-]{8,32})': 50,

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
            key_word = key_word.lower()
            if key_word in text:
                occurrences = [m.start() for m in re.finditer(re.escape(key_word), text)]
                text_score += len(occurrences)*score

        # If fast is set, skip pattern matching
        if not self.fast:
            for pattern, score in self.patterns.items():

                re_pattern = re.compile(pattern)
                matches = re_pattern.findall(text)

                if matches:
                    # only apply the match to the specific pattern once
                    text_score += len(matches)*score

        self.aggregate_score += text_score

        return text_score >= self.SCORE_THREASHOLD









