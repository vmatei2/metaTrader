import datetime
from datetime import timedelta
import requests
import pandas as pd
import config


MY_API_KEY = config.guardian_key
API_ENDPOINT = config.guardian_endpoint

my_params = {
    'q': 'crypto, bitcoin, stocks, economy',
    'from-date': "",
    'to-date': "",
    'order-by': "newest",
    'show-fields': '',
    'page-size': 10,
    'api-key': MY_API_KEY
}

def get_headlines(start_date, end_date):
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
                all_headlines.append(results_dict['webTitle'])
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

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date.today()
page_titles_dict = get_headlines(start_date, end_date)
results_df = create_df_from_dict(page_titles_dict)
stop = 0