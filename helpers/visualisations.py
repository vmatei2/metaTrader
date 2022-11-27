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


def bar_count_plot(sentiment_df):
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.countplot(x=sentiment_df["sentiment"], palette="rainbow_r")
    plt.title("News sentiment extracted from the Guardian News grouped by total value for each day", fontsize=18)
    for p in ax.patches:
        x = p.get_x() + p.get_width() / 2
        y = p.get_height()
        ax.annotate(y, (x, y), ha='center', va='center', fontsize=18, xytext=(0, 5), textcoords='offset points')
    label_fontsize=18
    plt.xticks(fontsize=label_fontsize)
    plt.yticks(fontsize=label_fontsize)
    plt.show()


sns.set_style("darkgrid")
price_df = pd.read_csv("../data/bitcoin_price_data.csv")
sentiment_df = pd.read_csv("../data/summed_sentiment.csv")
plot_price_sentiment_timeries(price_df, sentiment_df)
bar_count_plot(sentiment_df)
# plot_price_timeseries(price_df)