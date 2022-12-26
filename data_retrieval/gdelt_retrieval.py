import datetime
import pickle

import pandas as pd
from gdeltdoc import GdeltDoc, Filters
from get_guardian_headlines import apply_sentiment_analysis, group_and_sum_sentiment_by_days
from helpers.visualisations import print_full_df


def generate_spaced_entries(start_date, end_date):
    dates = []
    if isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date):
        for i in range(start_date.toordinal(), end_date.toordinal()):
            dates.append(datetime.date.fromordinal(i))
        return dates
    else:
        raise TypeError("Inputs should be in date time format")


def query_gdelt(date_list):
    gd = GdeltDoc()
    article_dict = {}
    timeine_dict = {}
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
            timeine_dict[date_list[i]] = gd.timeline_search("timelinetone", filters=f)
        save_dict("article_dict.txt", article_dict)
    if timeine_dict:
        save_dict("timeline_dict.txt", timeine_dict)
    return article_dict


def save_dict(filepath, dict_to_save):
    with open(filepath, 'wb') as f:
        pickle.dump(dict_to_save, f)
    return dict_to_save

def load_dict(filepath):
    with open(filepath, 'rb') as pickle_file:
        article_dict = pickle.load(pickle_file)
    return article_dict

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date.today()
date_list = generate_spaced_entries(start_date, end_date)
article_dict = query_gdelt(date_list)
#article_dict = load_dict("article_dict.txt")
timeline_dict = load_dict("timeline_dict.txt")
for key, value in timeline_dict.items():
    print_full_df(value)
concat_timeline_df = pd.concat(timeline_dict.values())
concat_timeline_df['Date'] = concat_timeline_df['datetime'].dt.date
timeline_df_by_day = group_and_sum_sentiment_by_days(concat_timeline_df, "../data/timeline_df_by_day.csv", "Average Tone")
test = 0

