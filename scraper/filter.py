
import re


class TextFilter(object):

    SCORE_THREASHOLD = 0

    # The score assigned to a discovered password in the resource file
    PASSWORD_DISCOVERY = 1000

    # Basic dictionary of key phrases and their associated values
    key_phrases = {

        # Common password dump indicators
        'password': 1000,
        'Password': 1000,
        'password dump': 1000,
        'dump': 50,
        'hack': 250,
        'crack': 250,
        'netstat': 100,
        'accounts': 200,
        'account': 200,
        'Admin': 100,
        'admin': 100,
        'pwd': 75,
        'SSN': 1000,
        'ssn': 1000,
        'pin': 1000,
        'PIN': 1000,
        'User': 500,
        'user': 500,
        'username': 500,
        'Username': 500,
        'Login': 500,
        'login': 500,
        'sudo': 500,
        'mysql': 500,
        'Mysql': 500,
        'MySQL': 500,
        'Postgres': 500,
        'postgres': 500,
        'root': 1000,

        # Common Logging patterns
        'INFO': -10,
        'ERROR': 10,
        'java': -10,
        'awt': -10,
        'security': 25,
        'javax': -10,


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
        '.rar': -50,
        '.rev': -50,



        # Domains
        '.net': -50,
        '.com': -50,
        '.co': -50,
        '.uk': -50,
        '.ca': -50,
        '.de': -50,
        '.ru': -50,

        # Path indicators
        '../': -10,
        '/home/': -10,
        '/src/': -10,

        # Code indicators
        'C++': -10,
        'Java': -10,
        'xml': -10,
        'XML': -10,
        '(': -10,
        ')': -10,
        'int': -10,
        '{': -10,
        '}': -10,
        '[': -10,
        ']': -10,
        '/': -10,
        '\\': -10,
        '.java': -10,
        '.py': -10,
        '::string': -10,
        '::int': -10,
        ';': -10,
        '++': -10,
        '+=': -10,
        '==': -10,
        '&&': -10,
        '||': -10,
        'Exception': -10,
        'exception': -10,
        'void': -10,
        'static': -10,
        'while': -10,
        'for': -10,
        'Object': -10,
        'class': -10,
        'Class': -10,
        'extends': -10,
        'public': -10,
        'private': -10,
        'protected': -10,
        '#': -10,
        'function': -10,
        'import': -10,
        '//': -10,
        '\\\\': -10,
        '=true': -10,
        '= true': -10,
        '= True': -10,
        '=True': -10,
        '=false': -10,
        '= false': -10,
        '= False': -10,
        '=False': -10,
        'echo': -10,
        'if': -10,
        'else': -10,
        'elif': -10,
        'else if': -10,
        '?xml': -10,
        'id=': -10,
        'class=': -10,
        '#include': -10,
        'main': -10,
        'long': -10,
        'float': -10,
        'cin': -10,
        'cout': -10,
        '>>': -10,
        '<<': -10,
        'print': -10,
        'printf': -10,
        '$': -10,
    }

    # Patterns (regular expressions) that, if matched, apply scores to the target.
    patterns = {

        # HTML Tags
        '(<.+?>)': -50,

        # Date / Time Stamps
        '((\d{1,2}|\d{4})[:-]\d{1,2}[:-](\d{4}|\d{1,2}))': -50,

        # Basic emails
        '[^@]+@[^@]+\.[^@]{1,5}': 250,



    }

    def apply_filter(self, text):

        text_score = 0

        for key_word, score in self.key_phrases.items():
            if key_word in text:
                text_score += score

        for pattern, score in self.patterns.items():

            re_pattern = re.compile(pattern)
            matches = re_pattern.findall(text)

            if matches:
                # only apply the match to the specific pattern once
                text_score += score

        return text_score









