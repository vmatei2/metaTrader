import numpy as np
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import normalize


def visualise_word_cloud(df, target_column):
    stopwords = set(STOPWORDS) # dataframe should already have stopwords removed, but worth checking no differences between wordcloud and nltk lists
    text = " ".join(i for i in df[target_column])
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def plot_price_timeseries(price_df):
    plt.figure(figsize=(10, 10))
    plt.plot(price_df["Close"])
    plt.xlabel("Days")
    plt.ylabel("Closing price")

def plot_price_sentiment_timeries(price_df, sentiment_df):
    plt.figure(figsize=(12, 10))
    norm_close = rescale_array(price_df["Close"])
    norm_sentiment = rescale_array(sentiment_df["sentiment"])
    plt.plot(norm_close, 'r')
    plt.plot(norm_sentiment, "b-")
    plt.legend(["Bitcoin Price", "Overall sentiment"])
    plt.xlabel("Days")
    plt.show()


def rescale_array(original_array):
    max = np.max(original_array)
    min = np.min(original_array)
    scaled_array = np.array([(x - min) / (max - min) for x in original_array])
    return scaled_array


sns.set_style("darkgrid")
price_df = pd.read_csv("../data/bitcoin_price_data.csv")
sentiment_df = pd.read_csv("../data/summed_sentiment.csv")
plot_price_sentiment_timeries(price_df, sentiment_df)
# plot_price_timeseries(price_df)