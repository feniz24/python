import requests
from twilio.rest import Client


def fetch_data():
    url = "https://rest.coinapi.io/v1/exchangerate/BTC/USD"
    headers = {
        "X-CoinAPI-Key": "11778CBE-1DA0-401A-92AE-1FF5D1C1A13F"
    }
    response = requests.get(url, headers=headers)
    return response.json()


account_sid = 'ACaab3c384918b2c518b553a4203237ce3'
auth_token = '07cad203ebbf76bf319c44d56f70955b'
client = Client(account_sid, auth_token)

data = fetch_data()
btc_price = data["rate"]

message = client.messages.create(
  from_='+12674294612',
  body=f"Today's price is {btc_price}",
  to='+959256030365'
)

print(message.sid)
