
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
        'clickjacking': 100,
        'clickjacked': 100,
        'trojan': 100,
        'trojanized': 100,
        'TROGANIZED': 100,
        'attackers': 150,
        'brute force': 250,
        'brute-force': 250,
        'leak': 100,
        'vulnerable': 100,
        'buffer overflow': 500,
        'SQL injection': 500,
        'authentication': 50,
        'remote admin access': 1000,
        'Cross-Site Scripting': 500,
        'user name': 500,
        'XSS': 500,
        'attack': 50,
        'administrator access': 1000,
        'administrator': 100,

        # Negative keywords
        'FlashPlayerPlugin': -250,
        'Adobe': -250,



        # Common Logging patterns
        'INFO': -10,
        'ERROR': 10,
        'java': -10,
        'awt': -10,
        'security': 25,
        'javax': -10,
        'main/INFO': -10,
        'WARN': -10,
        'Server': -10,


        # File extensions
        '.html': -100,
        '.mov': -100,
        '.htm': -100,
        '.png': -100,
        '.m3u8': -100,
        '.m3u8f': -100,
        '.zip': -100,
        '.jar': -100,
        '.php': -100,
        '.jpeg': -100,
        '.jpg': -100,
        '.inc': -100,
        '.mp4': -100,
        '.avi': -100,
        '.mkv': -100,
        '.rar': -100,
        '.rev': -100,
        '.exe': -100,
        '.ttf': -100,
        '.HDTV': -100,
        '.x264-C4TV': -100,
        '.WEB-DL.DD5.1.H.264': -100,
        '.dtd': -100,
        '.java': -100,
        '.py': -100,
        '.js': -100,
        'sql': -100,


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
        'www.': -50,

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
        '.widget': -10,
        '.plugin': -10,
        '.lib': -10,
        '.packet': -10,
        '.mods': -10,
        '.common': -10,
        'minecraft': -500,
        '\\\\Java': -10,
        'jre': -10,
        'java:': -10,
        'Integer': -50,
        'Double': -50,
        'parseInt': -50,
        'intValue': -50,
        'charAt': -50,
        'jquery': -50,
        'googleapis': -50,
        'src=': -50,
        '-Xmx1024m': -50,
        '-XX:MaxPermSize': -50,
        '-XX:PermSize': -50,
        '-XX:ParallelGCThreads': -50,
        '-XX:MinHeapFreeRatio': -50,
        '-XX:MaxHeapFreeRatio': -50,
        'Flash': -50,
        'Makefile': -50,
        'imgur': -50,
        'java.lang.NullPointerException': -50,
    }

    # Patterns (regular expressions) that, if matched, apply scores to the target.
    patterns = {

        # HTML Tags
        '(<.+?>)': -50,

        # Date / Time Stamps
        '((\d{1,2}|\d{4})[:/-](\d{1,2}|\w{2,3})[:/-](\d{4}|\d{1,2}))': -50,
        '(\[\d{2}:\d{2}\])': -50,
        # 18/Feb/2015

        # Basic emails
        '[^@]+@[^@]+\.[^@]{1,5}': 250,

        # Code
        '\w+\([\w\.\:=-]+\)?': -250,

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









