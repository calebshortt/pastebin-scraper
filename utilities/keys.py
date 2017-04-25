
"""
    Sometimes in pastebin, you may see private keys posted.
    This module helps manage the discovered keys and provides some utilities to try the discovered keys on
    encrypted text.
"""

import logging

from Crypto.PublicKey import RSA


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


class KMVars:
    RSA = 'rsa'


class KeyManager(object):

    key_paths = [
        ('keys/01.txt', KMVars.RSA),
    ]

    def __init__(self, key_path_list=None):
        if key_path_list and len(key_path_list) > 0:
            self.key_paths = key_path_list

    def _load_RSA_key(self, key_path):
        key = None
        with open(key_path, 'r') as f:
            key = f.read()

        r = None
        try:
            r = RSA.importKey(key)
        except ValueError:
            logger.info('Could not load RSA key from %s' % key_path)

        return r



if __name__ == "__main__":

    # http://www.laurentluce.com/posts/python-and-cryptography-with-pycrypto/

    test = KeyManager()._load_RSA_key('keys/01.txt')

    print test.can_encrypt()
    print test.can_sign()
    print test.has_private()    # Is public key
    # print test.public_key()
    print test.decrypt(test.encrypt('1234567890', 32))


