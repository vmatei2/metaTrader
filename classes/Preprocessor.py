import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class Preprocessing:
    def __init__(self):
        self.stopwords_en = set(stopwords.words('english'))
        self.stopwords_en.add("happened") # extremely common for headlines and does not convey info
        self.stopwords_en.add("say")

    def pre_process_string(self, string):
        word_tokens = word_tokenize(string)
        removed_stopwords_list = [w for w in word_tokens if not w in self.stopwords_en]
        removed_stopwords_string = ' '.join(removed_stopwords_list)
        return removed_stopwords_string
