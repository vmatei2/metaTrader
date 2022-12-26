import datetime
from datetime import timedelta

import numpy as np
import requests
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import config
from classes.Preprocessor import Preprocessing
from helpers.analysis import visualise_word_cloud

MY_API_KEY = config.guardian_key
API_ENDPOINT = config.guardian_endpoint

my_params = {
    'q': 'crypto OR bitcoin',  # AND: "," OR: "|" NOT: "-"
    'from-date': "",
    'to-date': "",
    'order-by': "newest",
    'show-fields': '',
    'page-size': 10,
    'api-key': MY_API_KEY
}


def get_headlines(start_date, end_date, pre_processor):
    dayrange = range((end_date - start_date).days + 1)
    page_titles_dict = {}
    all_dates = []
    all_headlines = []
    for daycount in dayrange:
        dt = start_date + timedelta(days=daycount)
        date_string = dt.strftime('%Y-%m-%d')
        print("Downloading", date_string)
        all_results = []
        my_params['from-date'] = date_string
        my_params['to-date'] = date_string
        current_page = 1
        total_pages = 1
        number_of_articles = 0
        while current_page <= total_pages:
            print("..page", current_page)
            my_params['page'] = current_page
            resp = requests.get(API_ENDPOINT, my_params)
            data = resp.json()
            response_results_dicts = data['response']['results']
            all_results.extend(response_results_dicts)
            for results_dict in response_results_dicts:
                headline = pre_processor.pre_process_string(results_dict['webTitle'])
                all_headlines.append(headline)
                number_of_articles += 1
            # if there is more than one page of results
            current_page += 1
            total_pages = data['response']['pages']
        date_list = [date_string]
        all_dates.append(date_list * number_of_articles)
    all_dates = [date for date_list in all_dates for date in date_list]
    page_titles_dict['Date'] = all_dates
    page_titles_dict['Headline'] = all_headlines
    return page_titles_dict


def create_df_from_dict(result_dict):
    results_df = pd.DataFrame.from_dict(result_dict)
    return results_df


def get_data(path_to_write):
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date.today()
    preprocessor = Preprocessing()
    page_titles_dict = get_headlines(start_date, end_date, preprocessor)
    results_df = create_df_from_dict(page_titles_dict)
    results_df.to_csv(path_to_write, index=False)
    return results_df


def apply_sentiment_analysis(df, target_column):
    sia_obj = SentimentIntensityAnalyzer()
    df["compound_sent"] = [sia_obj.polarity_scores(x)['compound'] for x in df[target_column]]
    conditions = [
        (df["compound_sent"] > 0.05),
        (df["compound_sent"] < -0.05),
        (df["compound_sent"] <= 0.05) & (df["compound_sent"] >= -0.05)
    ]
    values = [1, -1, 0]  # positive, negative, neutral sentiments
    df["sentiment"] = np.select(conditions, values)
    return df


def group_and_sum_sentiment_by_days(sentiment_df, write_path, column_name):
    sentiment_df = sentiment_df.groupby("Date").sum(column_name)
    sentiment_df.to_csv(write_path, index=True)
    return sentiment_df


if __name__ == '__main__':
    path = "../data/news_headlines.csv"
    results_df = pd.read_csv(path)
    visualise_word_cloud(results_df, 'Headline')
    results_df = apply_sentiment_analysis(results_df, 'Headline')
    group_and_sum_sentiment_by_days(results_df, "data/summed_sentiment.csv", "sentiment")
    stop = 0
