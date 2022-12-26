import numpy as np
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import normalize

from classes import Preprocessor
from classes.Preprocessor import Preprocessing


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
    fig, ax = plt.subplots(figsize=(14, 10))
    plt.plot(sentiment_df[target_column])
    plt.xlabel("Days", fontsize=14)
    plt.title(title, fontsize=18)
    plt.ylabel("Sentiment/Tone Value", fontsize=14)
    n = 14 # keep every nth label
    [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]
    plt.xticks(rotation=45)
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


def show_subplots(price_df, sentiment_df, target_column):
    fig, axs = plt.subplots(3, figsize=(16, 18))
    fig.suptitle("Plotting price time series and average tone evolution", fontsize=16)
    ylabel_fontsize=14
    title_fontsize=15
    axs[0].plot(price_df["Close"], 'r')
    axs[0].set_title("Bitcoin price evolution", fontsize=title_fontsize)
    axs[0].set_xlabel("Day")
    n = 14 # show every nth label xaxis
    prepare_axis(axs[0], n)
    axs[0].set_ylabel("Price", fontsize=ylabel_fontsize)
    axs[1].plot(sentiment_df[target_column])
    axs[1].set_title("Average tone from bitcoin related media", fontsize=title_fontsize)
    axs[1].set_ylabel("Tone value", fontsize=ylabel_fontsize)
    prepare_axis(axs[1], n)
    axs[2].plot(price_df["Returns"], 'y')
    axs[2].set_title("Bitcoin returns")
    axs[2].set_ylabel("Returns %", fontsize=ylabel_fontsize)
    prepare_axis(axs[2], n)
    fig.tight_layout()
    plt.show()


def prepare_axis(axis_obj, n):
    for index, label in enumerate(axis_obj.xaxis.get_ticklabels()):
        label.set_rotation(50)
        if index % n != 0:
            label.set_visible(False)

def returns_correlation(price_df, timeline_df, preprocessor):
    timeline_tone_series = timeline_df["Average Tone"]
    price_df = preprocessor.create_returns_column(price_df)
    price_series = price_df["Returns"]
    print("Correlation coefficient is: ")
    print(np.corrcoef(timeline_tone_series, price_series))


def main(price_df, timeline_df, preprocessor, sentiment_df=None):
    sns.set_style("darkgrid")
    returns_correlation(price_df, timeline_df, preprocessor)
    plot_price_sentiment_timeries(price_df, timeline_df, "Average Tone", "Normalized sentiment and price values")
    if sentiment_df:
        bar_count_plot(sentiment_df, "News sentiment grouped by day - extracted from the Guardian", "sentiment")
    # plot_price_timeseries(price_df)
    plot_sentiment_timeseries(timeline_df, "Average Tone", "Average Tone over analysed days")
    show_subplots(price_df, timeline_df, "Average Tone")



if __name__ == '__main__':
    main()
