from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime
import os

api_key = os.environ.get('PRIVATE_API_KEY')

global_url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'

parameters = {
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': api_key,
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(global_url, params=parameters)
  results = json.loads(response.text)
  # print(json.dumps(results, sort_keys=True, indent=4))
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

active_currencies = results['data']['active_cryptocurrencies']
global_cap = results['data']['quote']['USD']['total_market_cap']
bitcoin_percentage = results['data']['btc_dominance']
ethereum_percentage = results['data']['eth_dominance']
last_updated = results['data']['last_updated']

last_updated_string = datetime.fromisoformat(last_updated[:-1]).strftime('%d/%m/%Y as %H:%M')

print('Existem '+f'{active_currencies:,}'+' criptomoedas ativas no mercado.')
print('O MarketCap de criptomoedas eh de '+
        f'{global_cap:,}'+' USD')
print('Bitcoin representa '+f'{bitcoin_percentage:.2f}'+'% do mercado.')
print('Ethereum representa '+f'{ethereum_percentage:.2f}'+'% do mercado.')
print('Atualizado: '+last_updated_string+' UTC.')
