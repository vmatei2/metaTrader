import datetime
import pickle

import pandas as pd
from gdeltdoc import GdeltDoc, Filters
from helpers.analysis import print_full_df


def generate_spaced_entries(start_date, end_date):
    dates = []
    if isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date):
        for i in range(start_date.toordinal(), end_date.toordinal()):
            dates.append(datetime.date.fromordinal(i))
        return dates
    else:
        raise TypeError("Inputs should be in date time format")

def group_and_sum_sentiment_by_days(sentiment_df, write_path, column_name):
    sentiment_df = sentiment_df.groupby("Date").sum(column_name)
    sentiment_df.to_csv(write_path, index=True)
    return sentiment_df

def query_gdelt(start_date, end_date):
    date_list = generate_spaced_entries(start_date, end_date)
    gd = GdeltDoc()
    article_dict = {}
    timeline_dict = {}
    for i in range(len(date_list)):
        # each entry in the data frame will contain news for a week - split up in order to avoid limitations of the
        # gdelt api (250 returns)
        if i % 7 == 0:
            start_date = str(date_list[i])
            if (i+6 > len(date_list)):
                end_date = str(date_list[-1])  # if the date goes out of bounds, then simply get from now up until max
                # point of the date list
            else:
                end_date = str(date_list[i + 6])
            f = Filters(
                keyword="bitcoin",
                start_date=start_date,
                end_date=end_date,
                country=["UK", "US"]
            )
            # article_dict[start_date] = gd.article_search(filters=f)
            timeline_dict[date_list[i]] = gd.timeline_search("timelinetone", filters=f)
        save_dict("article_dict.txt", article_dict)
    if timeline_dict:
        save_dict("timeline_dict.txt", timeline_dict)
        concat_timeline_df = pd.concat(timeline_dict.values())
        concat_timeline_df['Date'] = concat_timeline_df['datetime'].dt.date
        timeline_df_by_day = group_and_sum_sentiment_by_days(concat_timeline_df, "../data/timeline_df_by_day.csv", "Average Tone")
    return timeline_df_by_day


def save_dict(filepath, dict_to_save):
    with open(filepath, 'wb') as f:
        pickle.dump(dict_to_save, f)
    return dict_to_save

def load_dict(filepath):
    with open(filepath, 'rb') as pickle_file:
        article_dict = pickle.load(pickle_file)
    return article_dict


def main():
    pass

