import requests
import json

currencyBase = input("from: ")
currencyTo = input("to: ")
amount = input("amount ")


response = requests.get("https://api.exchangeratesapi.io/latest?base={}".format(currencyBase))

data = json.loads(response.text)

print(json.dumps(data, indent = 4))
print(data["rates"][currencyTo])
finalAmount = int(amount)*data["rates"][currencyTo]
print(round(finalAmount, 2))