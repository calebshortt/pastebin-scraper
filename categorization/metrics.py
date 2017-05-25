

class VALUES:
    CHARSET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-=!@#$%^&*()_+/?\\|\'"]}[{'


class FrequencyAnalysis(object):

    def __init__(self):
        pass

    def analyze(self, text):

        results = {}
        text = list(text)

        text_set = set(VALUES.CHARSET)

        for item in text_set:
            if item in text:
                results[item] = text.count(item)

        return results


if __name__ == "__main__":
    fa = FrequencyAnalysis()
    print fa.analyze("testing123123123 this is a test")




