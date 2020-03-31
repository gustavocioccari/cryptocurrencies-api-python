from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime
import os

api_key = os.environ.get('PRIVATE_API_KEY')

converter_url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'

crypto_to_convert=str(input('Qual criptomoeda deseja converter: Bitcoin, Ethereum ou Litecoin? '))
currency=str(input('Para qual moeda deseja converter?(Utilize o formato: USD) '))
amount=input('Quanto deseja converter? ')
currency=currency.upper()
crypto_to_convert=crypto_to_convert.lower()
if crypto_to_convert == 'bitcoin':
    parameters = {
      'id':'1',
      'amount':amount,
      'convert':currency,
    }
    crypto_to_convert='BTC'
elif crypto_to_convert == 'litecoin':
    parameters = {
      'id':'2',
      'amount':amount,
      'convert':currency,
    }
    crypto_to_convert='LTC'
elif crypto_to_convert == 'ethereum':
    parameters = {
      'id':'1027',
      'amount':amount,
      'convert':currency,
    }
    crypto_to_convert='ETH'

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': api_key,
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(converter_url, params=parameters)
  results = json.loads(response.text)
  print(json.dumps(results, sort_keys=True, indent=4))
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

conversion = results['data']['quote'][currency]['price']
last_updated = results['data']['last_updated']

last_updated_string = datetime.fromisoformat(last_updated[:-1]).strftime('%d/%m/%Y as %H:%M')

print(amount+crypto_to_convert+' = '+f'{conversion:,.2f}'+currency)
print('Cotacao obtida em: '+last_updated_string)
