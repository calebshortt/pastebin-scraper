
import re


class FileParser(object):

    def parse_email_pw_file(self, path, separator=':'):
        """
        Parses the given file and looks for <email>:<password> combinations (on each line)
        :param path:
        :return: list of tuples (results: [ (<email>, <password>), ...] )
        """
        results = []

        with open(path) as f:
            content = f.readlines()

        for line in content:
            pattern = '([^@]+@[^@]+\.[^@]{1,5})' + separator + '([\w\S^"]+)'
            match = re.match(pattern, line.strip().replace(' ', ''))

            if match:
                results.append((match.group(1), match.group(2)))

        return results


p = FileParser()
results = p.parse_email_pw_file('../resources/test.txt', ':')

for result in results:
    print result[1]

