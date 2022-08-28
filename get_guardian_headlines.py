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