from fyers_api import fyersModel
import json

tokenFile = open('./store_token.json')
tokenJson = json.load(tokenFile)
access_Token = tokenJson['access_token']

# apiCredFile = open("./api")
ClientID = "TU9RDXY8QS-100"

fyers = fyersModel.FyersModel(client_id=ClientID, token= access_Token)
symbol = {'symbols': 'NSE:NIFTYBANK-INDEX'}
data=(fyers.quotes(symbol))
print(type(data))
print(data['d'][0]['v']['ask'])