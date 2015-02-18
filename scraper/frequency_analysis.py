

class PWAnalyzer(object):

    def __init__(self):
        self.current_results = {}
        self.previously_loaded_paths = []
        self.total_sum = None

    def count_chars(self, text):
        """
        Takes a string (text) and counts the number of characters there are.
        Updates the current_results variable and returns the results of the given text.
        :param text:
        :return: results from text: dict
        """
        local_results = {}

        for ch in text:
            self._add_char_to_dict(ch, local_results)
            self._add_char_to_dict(ch, self.current_results)

        return local_results

    def _add_char_to_dict(self, ch, count_dict):
        if ch in count_dict:
            count_dict[ch] += 1
        else:
            count_dict[ch] = 1

        return count_dict

    def get_frequency(self, ch):
        """
        Calculates the current frequency of the character in the current results set.

        :param ch:
        :return: float result: a percentage-based frequency based on the total character count.
        """

        if not self.total_sum:
            self.total_sum = sum([item for item in self.current_results.values()])

        target = self.current_results.get(ch, 0)
        result = float(target)/float(self.total_sum)

        return result

    def import_resource(self, path='resources/passwords.txt'):
        """
        Imports a given resource (file with a list of passwords/text) to be analyzed.
        Required the file to be formatted with one entry per line.

        :param path:
        :return:
        """
        with open(path) as f:
            content = f.readlines()

        # Prevent multiple entries of the same resource (will skew frequency distributions)
        if path not in self.previously_loaded_paths:
            self.previously_loaded_paths.append(path)
            [self.count_chars(line.strip()) for line in content]

        self.total_sum = sum([item for item in self.current_results.values()])

    def calculate_weighted_value(self, text, max_value):
        """
        Calculate the weighted score of the given text based on the generated frequency analysis and a max_value.
        :param text:
        :param max_value: Maximum value available (a 100% frequency would apply the entire value, 50% is half, etc)
        :return: weighted value (int)
        """

        # Each character in the text gets an equal portion of max value before weighting
        per_char__max_value = max_value / len(text)

        weighted_value = 0

        for ch in text:
            freq = self.get_frequency(ch)
            weighted_value += per_char__max_value * freq

        return weighted_value


#
# a = PWAnalyzer()
# a.import_resource('../resources/passwords.txt')
#
# sorted_list = sorted(a.current_results.items(), key=lambda ch_tuple: ch_tuple[1])
#
# for ch, freq in sorted_list:
#     print '{}: {}'.format(ch, freq)
#
# print 'frequency for e and 1: {}, {}'.format(a.get_frequency('e'), a.get_frequency('1'))












