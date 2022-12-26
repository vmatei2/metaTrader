import datetime

import pandas as pd
from classes.Preprocessor import Preprocessing
from helpers import analysis
from data_retrieval import get_bitcoin_data
from data_retrieval import gdelt_retrieval
import os

class Controller:
    def __init__(self, start_date, end_date, symbol):
        self.start_date = start_date
        self.end_date = end_date
        self.symbol = symbol
        self.bitcoin_price_path = "data/bitcoin_price_data.csv"
        self.gdelt_timeline_data_path = "data/timeline_df_by_day.csv"
        self.bitcoin_df = pd.DataFrame()
        self.gdelt_timeline_df = pd.DataFrame()
        self.preprocessor = Preprocessing()

    def retrieve_data(self):
        bitcoin_price_df = get_bitcoin_data.retrieve_bitcoin_data(self.symbol, self.start_date.strftime("%d-%m-%Y"), self.end_date("%d-%m-%Y"), self.bitcoin_price_path)
        gdelt_df = gdelt_retrieval.query_gdelt(self.start_date, self.end_date)
        return bitcoin_price_df, gdelt_df

    def load_data(self):
        if os.path.exists(self.bitcoin_price_path) and os.path.exists(self.gdelt_timeline_data_path):
            self.bitcoin_df = pd.read_csv(self.bitcoin_price_path, index_col=0)
            self.gdelt_timeline_df = pd.read_csv(self.gdelt_timeline_data_path, index_col=0)
        else:
            self.bitcoin_df, self.gdelt_timeline_df = self.retrieve_data()

    def run_analysis(self):
        analysis.main(self.bitcoin_df, self.gdelt_timeline_df, self.preprocessor)

    def run(self):
        self.load_data()
        self.run_analysis()


controller = Controller(datetime.date(2022, 1, 1), datetime.date.today(), "BTC")
controller.run()