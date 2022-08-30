from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set_style('white')

def visualise_word_cloud(df, target_column):
    stopwords = set(STOPWORDS) # dataframe should already have stopwords removed, but worth checking no differences between wordcloud and nltk lists
    text = " ".join(i for i in df[target_column])
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


