import numpy as np
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import normalize


def visualise_word_cloud(df, target_column):
    stopwords = set(
        STOPWORDS)  # dataframe should already have stopwords removed, but worth checking no differences between wordcloud and nltk lists
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


def plot_sentiment_timeseries(sentiment_df, target_column, title):
    plt.figure(figsize=(10, 10))
    plt.plot(sentiment_df[target_column])
    plt.xlabel("Days", fontsize=14)
    plt.title(title, fontsize=18)
    plt.ylabel("Sentiment/Tone Value", fontsize=14)
    plt.show()


def plot_price_sentiment_timeries(price_df, sentiment_df, target_column, title):
    plt.figure(figsize=(12, 10))
    norm_close = rescale_array(price_df["Close"])
    norm_sentiment = rescale_array(sentiment_df[target_column])
    plt.plot(norm_close, 'r')
    plt.plot(norm_sentiment, "b-")
    plt.legend(["Bitcoin Price", "Overall sentiment"], fontsize=12)
    plt.xlabel("Days", fontsize=14)
    plt.ylabel("Normalized values", fontsize=16)
    plt.title(title, fontsize=18)
    plt.show()


def rescale_array(original_array):
    max = np.max(original_array)
    min = np.min(original_array)
    scaled_array = np.array([(x - min) / (max - min) for x in original_array])
    return scaled_array


def bar_count_plot(sentiment_df, title, target_column):
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.countplot(x=sentiment_df[target_column], palette="rainbow_r")
    plt.title(title, fontsize=18)
    for p in ax.patches:
        x = p.get_x() + p.get_width() / 2
        y = p.get_height()
        ax.annotate(y, (x, y), ha='center', va='center', fontsize=18, xytext=(0, 5), textcoords='offset points')
    label_fontsize = 18
    plt.xticks(fontsize=label_fontsize)
    plt.yticks(fontsize=label_fontsize)
    plt.show()



def print_full_df(x):
    """
    Function used to simply print the full dataframe as saving and
    loading from pickled df with the format returned by GDelt's timeline
    search seems to cause issues
    https://stackoverflow.com/questions/38956660/dataframe-not-showing-in-pycharm
    :param x:
    :return:
    """
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


def two_by_one_plot(price_df, sentiment_df, target_column):
    fig, axs = plt.subplots(2)
    fig.suptitle("Plotting price time series and average tone evolution")
    axs[0].plot(price_df["Close"], 'r')
    axs[0].set_title("Bitcoin price evolution")
    axs[0].set_xlabel("Day")
    axs[0].set_ylabel("Price")
    axs[1].plot(sentiment_df[target_column])
    axs[1].set_title("Average tone from bitcoin related media")
    axs[1].set_ylabel("Tone value")
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    sns.set_style("darkgrid")
    price_df = pd.read_csv("../data/bitcoin_price_data.csv")
    sentiment_df = pd.read_csv("../data/summed_sentiment.csv")
    timeline_df = pd.read_csv("../data/timeline_df_by_day.csv", index_col=0)
    plot_price_sentiment_timeries(price_df, timeline_df, "Average Tone", "Normalized sentiment and price values")
    bar_count_plot(sentiment_df, "News sentiment grouped by day - extracted from the Guardian", "sentiment")
    # plot_price_timeseries(price_df)
    plot_sentiment_timeseries(timeline_df, "Average Tone", "Average Tone over analysed days")
    two_by_one_plot(price_df, timeline_df, "Average Tone")
    print("Correlation between the two arrays is: ")