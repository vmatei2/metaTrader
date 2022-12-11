import datetime
from gdeltdoc import GdeltDoc, Filters


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
        if i % 7 == 0:
            start_date = str(date_list[i])
            end_date = str(date_list[i + 6])
            f = Filters(
                keyword="bitcoin",
                start_date=start_date,
                end_date=end_date,
                country=["UK", "US"]
            )
            article_dict[start_date] = gd.article_search(filters=f)
    return article_dict



start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 10, 1)
date_list = generate_spaced_entries(start_date, end_date)
article_dict = query_gdelt(date_list)

# Search for articles matching the filters
articles = gd.article_search(f)
# get a timeline of the number of articles matching the filters
timeline = gd.timeline_search("timelinetone", f)

breakhere = 0
