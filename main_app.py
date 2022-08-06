# import the required packages
from flask import Flask, request, make_response
import time
import requests
import socket
from collections import OrderedDict
import json

app = Flask(__name__)

# app route in case someone visits the home url
@app.route("/", methods=['GET'])
def home():   
    answers = socket.getaddrinfo('paxful.com', 443)
    (family, type, proto, canonname, (address, port)) = answers[0]
    s = requests.Session()
    headers = OrderedDict({
        'Host': "paxful.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
    })
    s.headers = headers
    data = s.get(f"https://{address}/rest/v1/offers?camelCase=1&user_badges%5B0%5D=7&user_badges%5B1%5D=8&user_badges%5B2%5D=2&user_badges%5B3%5D=1&user_badges%5B4%5D=5&withFavorites=false&crypto_currency_id=1&is_payment_method_localized=0&visitor_country_has_changed=false&visitor_country_iso=IN&payment-method%5B0%5D=with-any-payment-method&type=sell", headers=headers, verify=False).text
    #data=requests.get(url, headers=headers).content.decode()
    data=json.loads(data)

    response = make_response(data)

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.status_code = 200
    response.mimetype = 'application/json'
    return response


# Call to run the app if the current file is directly executed
if __name__ == "__main__":
    app.run(debug=True)