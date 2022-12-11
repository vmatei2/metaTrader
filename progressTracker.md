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
  

27th November:
- Added visualisation of sentiment from all days based on summation
- Have future ideas which need to be actioned
- Looking into a Trello board so I can split up/pick up work as/when I have on time on this
- Very interesting to see from the visualisation that most days at the moment group together around 
-1,0,1
  
  - However, in the days which appear as outliers, we are more likely to see negative sentiment, rather than positive
  - Can this be related to the Guardian/news outlets in general looking to dramaticise their headlines attempting to get clicks?
  - Plus, what type of effect can this have on our data/future results? Interesting exploration areas
  
11th December

- Connecting to GDELT api to retrieve news articles
- Querying for Bitcoin articles atm
- Very useful tool, also offering sentiment retreival
- Interesting to couple this with our sentiment analysis and compare results
- Retrieve for articles from start of 2022

GDelt = supported by Google Jigsaw, the GDELT project monitors the world's broadcast
print and web news from nearly every corner of every country in over 100 langauges
and identifies the poeple, locations, orgs, themes, sources emotions, counts,
quotes, images and events driving our global society every second of every day

GDelt monitors the world's news media from nearly every corner of every country in print,
broadcast and web formats, in over 100 languages, every moment of every day

Its historical archive stretches back to Jan 1 1979 and updates every 15 mins
