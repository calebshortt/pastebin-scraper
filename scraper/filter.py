
import re
import logging


class TextFilter(object):

    SCORE_THREASHOLD = 0

    aggregate_score = 0

    # Basic dictionary of key phrases and their associated values
    key_phrases = {

        # Common password dump indicators
        'password': 1000,
        'login': 1000,
        'logins': 1000,
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


        # Domains
        '.net': -50,
        '.com': -50,
        '.co': -50,
        '.uk': -50,
        '.ca': -50,
        '.de': -50,
        '.ru': -50,


        # Code Filters
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
        '': -50,

        # HTML/CSS filters
        'px;': -50,
        'container': -50,
        '.Text': -50,
        ':hover': -50,
        'scroll': -50,
        'text': -50,
        'Button': -50,
        'toggle': -50,


        # General Negative Phrases
        'Minecraft': -50,
        'C:\Windows\system32': -50,
    }

    # Patterns (regular expressions) that, if matched, apply scores to the target.
    patterns = {

        # HTML Tags
        '(<.+?>)': -50,

        # Date / Time Stamps
        '((\d{1,2}|\d{4})[:-]\d{1,2}[:-](\d{4}|\d{1,2}))': -50,

    }

    def apply_filter(self, text):

        text_score = 0
        # text = text.lower()

        for key_word, score in self.key_phrases.items():
            if key_word in text:
                text_score += score

        for pattern, score in self.patterns.items():

            re_pattern = re.compile(pattern)
            matches = re_pattern.findall(text)

            if matches:
                # only apply the match to the specific pattern once
                text_score += score

        self.aggregate_score += text_score

        return text_score >= self.SCORE_THREASHOLD









