from nltk.corpus import stopwords


class Preprocessing:
    def __init__(self):
        self.stopwords_en = set(stopwords.words('english'))
