
def load_corpus(path):

    text = ""
    with open(path, 'r') as f:
        text = f.read()

    return text
