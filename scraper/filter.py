

class TextFilter(object):

    # Basic dictionary of key phrases and their associated values
    key_phrases = {

        # Common password dump indicators
        'password': 100,
        'password dump': 100,
        'dump': 50,
        'hack': 50,
        'crack': 50,
        'netstat': 50,
        'accounts': 50,


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


        # Domains
        '.net': -50,
        '.com': -50,
        '.co': -50,
        '.uk': -50,
        '.ca': -50,
        '.de': -50,
        '.ru': -50,


    }


    # Patterns (regular expressions) that, if matched, apply scores to the target.
    patterns = {

        # HTML Tags
        '(<.+?>)': -50,

        # Date / Time Stamps
        '((\d{1,2}|\d{4})[:-]\d{1,2}[:-](\d{4}|\d{1,2}))': -50,

    }