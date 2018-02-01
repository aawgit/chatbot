from flask import Flask, request, jsonify
import json
import requests
import os
from datetime import date
import string

app = Flask(__name__)
port = int(os.environ["PORT"])
print(port)

date = date.today()
print("date is %s %s" %(date,date))

@app.route('/', methods=['POST'])
def index():
  print(port)
  data = json.loads(request.get_data().decode('utf-8'))

  # FETCH THE CRYPTO NAME
  
##  crypto_name = data["nlp"]["entities"]["crypto_name"][0]["raw"]#data['nlp']['entities']['crypto_name']['raw']
##  print(data["nlp"]["entities"]["crypto_name"][0]["raw"])

  # FETCH THE INTENT
  
  intent = data["nlp"]["intents"][0]["slug"]
  print(intent)
 

  # FETCH BTC/USD/EUR PRICES
  #r = requests.get("https://min-api.cryptocompare.com/data/price?fsym="+crypto_name+"&tsyms=BTC,USD,EUR")

##  return jsonify(
##    status=200,
##    replies=[{
##      'type': 'text',
##      'content': 'The price of %s is %f BTC and %f USD' % (crypto_name, r.json()['BTC'], r.json()['USD'])
##    }]
##  )

  if intent == "commodity_prices":
    #Fetch the metal
    metal = (str(data["nlp"]["entities"]["metal"][0]["raw"])).lower()

    #Metal key dictionary
    metals = {'tin':'LME/PR_TN', 'copper':'LME/AB_CU', 'aluminium':'LME/AB_AL', 'aluminum':'LME/AB_AL', 'gold':'LBMA/GOLD','silver':'LBMA/SILVER', 'cobolt':'LME/PR_CO', 'zinc':'LME/AB_ZI'}

    #Unit dictionary
    units =  {'tin':'USD/tonne', 'copper':'USD/tonne','aluminium':'USD/tonne', 'aluminum':'USD/tonne','gold': 'USD/Troy ounce', 'silver': 'USD/Troy ounce', 'cobolt':'USD/tonne', 'zinc':'USD/tonne'}

    metal_key = metals[metal]
    unit = units[metal]
    print(metal_key)

    #Fetch metal price
    #url = "https://www.quandl.com/api/v3/datasets/LME/AB_CU?start_date=%s&end_date=%s&api_key=QMv17KPWdYzFzydoL5Sz"%(date, date)
    url = "https://www.quandl.com/api/v3/datasets/%s?start_date=%s&end_date=%s&api_key=QMv17KPWdYzFzydoL5Sz"%(metal_key, date, date)
    print(url)    
    r =requests.get(url)
    date2 = r.json()["dataset"]["newest_available_date"]
    url = "https://www.quandl.com/api/v3/datasets/%s?start_date=%s&end_date=%s&api_key=QMv17KPWdYzFzydoL5Sz"%(metal_key, date2, date2)
    print(url)
    r = requests.get(url)
    print(r.json())
    price = r.json()["dataset"]["data"][0][1]
    return jsonify(
        status=200,
        replies=[{
          'type': 'text',
          #'content': 'The intent is %s' %(intent)
          #'content': 'Would you like to know %s price?' %(metal)
          'content': '%s price is %s %s as at %s' %(metal, price, unit, date2)
        }]
      )

@app.route('/errors', methods=['POST'])
def errors():
  print(json.loads(request.get_data()))
  return jsonify(status=200)

app.run(port=port, host="0.0.0.0")

#https://www.quandl.com/api/v3/datasets/LME/AB_CU?start_date=2018-01-25&end_date=2018-01-25&api_key=QMv17KPWdYzFzydoL5Sz

