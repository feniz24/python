import requests
from datetime import date, timedelta
from twilio.rest import Client

STOCK = "IBM"
COMPANY_NAME = "IBM Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API = ""
NEWS_API = ""

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "IBM",
    "apikey": STOCK_API,
}

news_parameters = {
    "qInTitle": STOCK,
    "apiKey": NEWS_API,
}

yesterday_date = str(date.today() - timedelta(days=1))
day_before_yesterday = str(date.today() - timedelta(days=2))

response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo")
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

yesterday_price = float(data_list[0]["4. close"])
day_before_yesterday_price = float(data_list[1]["4. close"])
price_difference = abs(yesterday_price - day_before_yesterday_price)
percent_price = (price_difference * 100) / day_before_yesterday_price
if yesterday_price > day_before_yesterday_price:
    price = f"🔺{percent_price}%"
else:
    price = f"🔻 {percent_price}%"

if percent_price > 5:
    response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    data = response.json()
    articles = data["articles"][:3]

    account_sid = 'ACaab3c384918b2c518b553a4203237ce3'
    auth_token = '07cad203ebbf76bf319c44d56f70955b'
    client = Client(account_sid, auth_token)
    message_text = ""
    for article in articles:
        message_text = f"{STOCK} {price} \nHeadline: {article['title']}\n Brief: {article['description']}"
        message = client.messages.create(
            from_='',
            body=message_text,
            to=''
        )

        print(message.sid)
