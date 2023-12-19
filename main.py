import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "P7FEEGDXXECOBSTM"
NEWS_API_KEY = "1c5a322ed48b46e39bae5f45f649dffb"
TWILIO_SID = "ACf6182316b77bff0c353731f9e92c8cfa"
TWILIO_AUTH_TOKEN = "45c845d41fc6bcdb324a6c708d11e7fb"

stock_params = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(difference)

diff_percent = (difference / float(yesterday_closing_price)) * 100
print(diff_percent)

if diff_percent > 1:
    news_params = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

# Use Python slice operator to create a list that contains the first 3 articles
    three_articles = articles[:3]

# create a new list of the first 3 article's headline and description using list comprehension
    formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
# Send each article as a separate message via Twilio
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
# Send each article as a seperate mesaage via Twilio
    for article in formatted_articles:
        message = client.messages.create(
            body = article,
            from = "+15167306982",
            to="+9947608507"
    )


