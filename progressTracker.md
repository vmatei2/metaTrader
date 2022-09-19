19th September:

- Retrieving Bitcoin price data from CoinMarketCap scraper
- Already have the sentiment data, with initial analysis via VADER
- Grouped headlines by date and summed the sentiment score
- Rescaled the two arrays and plotted together to observe if there is some initial correlation
- Results are hard to read because of the high volatility of Bitcoin, but have ideas to continue the work

#### To Do
- Add column to the bitcoin price data which is simply either 1 or -1, depending
on the direction in which the price moved
- Further re-fine the Vader analysis
    - Maybe add more words to the lexcion?
    - Look for different threshold values that provide better opportunity to understand
    the headline data
  
- Very important to find another data source, currently not enough information
    - Ask Humzah for the library we used in TTDS, could be very helpful