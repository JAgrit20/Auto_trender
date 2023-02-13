import json
import requests
import pandas as pd
from fyers_api import fyersModel
from fyers_api import accessToken
import json


def getCurrentPCR(symbol):
    url = 'https://www.nseindia.com/api/option-chain-indices?symbol='+symbol
    headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'accept-encoding' : 'gzip, deflate, br',
    'accept-language' : 'en-US,en;q=0.9'
    }
    response = requests.get(url, headers=headers).content
    data = json.loads(response.decode('utf-8'))
    # print(data)

    price = data['filtered']['data'][0]['PE']['underlyingValue']


    print("totCE",price)

    return price


ClientID = "TU9RDXY8QS-100"
AppID = "TU9RDXY8QS-100"
SecretID = "9FL2VROLMN"
RedirectURI="http://127.0.0.1:8000/api/fyers_success"
response_type= "success"

acc_t="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE2NzYyNjg0OTMsImV4cCI6MTY3NjI5ODQ5MywibmJmIjoxNjc2MjY3ODkzLCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJYQTQyMzY0Iiwib21zIjpudWxsLCJub25jZSI6IiIsImFwcF9pZCI6IlRVOVJEWFk4UVMiLCJ1dWlkIjoiMWM5MGRmMDA2ODcyNDJmZmEzYzNiZmQwYzYyYjNjYWMiLCJpcEFkZHIiOiIwLjAuMC4wIiwic2NvcGUiOiIifQ.uJOqMqpJlg2npJivnxyL4OoaoPG5_5ih_zEBwRqU52k"
# accessToken="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2NzYyNjgwNDMsImV4cCI6MTY3NjMzNDY0MywibmJmIjoxNjc2MjY4MDQzLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCajZkSUxMRlJyUW1tYXJQakFKTG9vY0RkVl9nZnlSclFRdzY5eV9IM05NTlMxRk55T0V6OFNfeGxHU3V4R2k5am8ya1VBN3RrM0pwU1QwZFhsT2FvbU5aS0hjRDRKYm9ETk1aZVhzMW91cFgwLUJMST0iLCJkaXNwbGF5X25hbWUiOiJBRElUWUEgUkFNTkFUSCBTSElOREUiLCJvbXMiOm51bGwsImZ5X2lkIjoiWEE0MjM2NCIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.MQU0FPrL48gidkpkH6glwXlFzizXMIyIpid1SH6wVdw"

# fyers = fyersModel.FyersModel(client_id=client_id, token= token)
# symbol = {'symbols': 'NSE:TATAMOTORS-EQ'}
# print(fyers.quotes(symbol))

session = accessToken.SessionModel(
    client_id = ClientID,
    secret_key = SecretID,
    redirect_uri = RedirectURI,
    response_type = "code",
    grant_type = "authorization_code",
    state = response_type
)

url = session.generate_authcode()
print(url)

auth_code = input("Enter auth code:")
session.set_token(auth_code)
token_response = session.generate_token()
print(token_response)

token_response_obj = json.dumps(token_response,indent= 4)

with open("store_token.json","w") as outfile:
    outfile.write(token_response_obj)
