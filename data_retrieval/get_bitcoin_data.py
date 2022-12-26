from cryptocmd import CmcScraper
### Cmc scraper retrieves data from CoinMarketCap
import datetime

def retrieve_bitcoin_data(symbol, start_date, end_date, write_path):
    scraper = CmcScraper(symbol, start_date, end_date)
    bitcoin_price_df = scraper.get_dataframe()
    bitcoin_price_df = bitcoin_price_df[::-1]  #  reverse the dataframe, currently returned with
    bitcoin_price_df = bitcoin_price_df.set_index("Date")
    bitcoin_price_df.to_csv(write_path, index=True)
    return bitcoin_price_df



