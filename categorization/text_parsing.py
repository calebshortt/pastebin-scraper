
import hashlib

from metrics import FrequencyAnalysis


class CONSTANTS:
    HASH = 'hash'
    BASIC_FREQ = 'basic_frequencies'

    # flag constants
    KEY_FLAG = 'flag'
    PW_DUMP = 'pwdump'              # Classic PW dump <user>:<pass>
    BUSY_PW_DUMP = 'busypwdump'     # PW Dump with a lot of noise / text interweaved

    # Categorizations of text:    "label": <categorization>     ex: "label": "code"
    KEY_LABEL = 'label'
    CODE = 'code'
    ENCRYPTED = 'enc'
    LOG = 'log'
    CONFIG = 'config'


class Digestor(object):

    """

    Take text in, hash it, run metrics on it, return metrics and hash

    Have some helper functions to check if text has been seen before (check hash, etc)

    """

    freq_analysis = None

    def __init__(self):
        self.freq_analysis = FrequencyAnalysis()

    def digest(self, text, normalized=True):

        results = {}

        results[CONSTANTS.HASH] = self.get_hash(text)

        freqs = self.freq_analysis.analyze(text)
        if normalized and freqs:
            max_count = max(dict(freqs).values())
            temp = {}
            for key, value in freqs.items():
                temp[key] = float(value)/max_count

            freqs = temp

        results[CONSTANTS.BASIC_FREQ] = freqs

        return results

    def get_hash(self, text):
        text = text.encode('utf-8')
        h = hashlib.sha512()
        h.update(text)
        return h.hexdigest()








