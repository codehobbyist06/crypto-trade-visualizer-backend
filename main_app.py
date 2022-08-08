# import the required packages
from flask import Flask, request, make_response
import time
import requests
import socket
from collections import OrderedDict
import json

app = Flask(__name__)

# app route in case someone visits the home url


@app.route("/", methods=['POST', 'GET'])
def home():
    answers = socket.getaddrinfo('paxful.com', 443)
    (family, type, proto, canonname, (address, port)) = answers[0]
    s = requests.Session()

    headers = OrderedDict({
        'Host': "paxful.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
    })
    s.headers = headers

    try:
        username = request.args.get('username')
    except Exception as e:
        response = make_response(
            {"status": "error", "message": f"Could not find username in the args"})
        print({"status": "error", "message": f"Could not find username in the args"})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    offset = 1

    if username == "" or username == None:
        response = make_response(
            {"status": "error", "message": "No username found!"})
        print({"status": "error", "message": "No username found!"})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    url_for_user_offers = f"https://{address}/rest/v1/users/{username}/active-offers?transformResponse=camelCase&type=buy&offset={offset}"

    url_for_user_info = f"https://paxful.com/rest/v1/users/{username}?transformResponse=camelCase"

    user_data = s.get(url_for_user_info, headers=headers, verify=False).text
    user_data = json.loads(user_data)

    # print(user_data['data'])

    user_data_last_seen = user_data['data']['lastSeenString']
    user_data_trades_count = user_data['data']['countTrades']

    offers_data = s.get(url_for_user_offers,
                        headers=headers, verify=False).text
    offers_data = json.loads(offers_data)

    total_offers_data = []

    for data in offers_data['data']:
        new_offer = {
            "username": username,
            "last_seen": user_data_last_seen,
            "ad_name": data['paymentMethodName'],
            "amount": round(data['fiatPricePerCrypto'], 2),
            "total_trades": user_data_trades_count,
            "currency_code": data['fiatCurrencyCode'],
        }
        total_offers_data.append(new_offer)

    while offers_data['meta']['hasMorePages'] == True:
        offset = offset + 1
        url_for_user_offers = f"https://{address}/rest/v1/users/{username}/active-offers?transformResponse=camelCase&type=buy&offset={offset}"
        offers_data = s.get(url_for_user_offers,
                            headers=headers, verify=False).text
        offers_data = json.loads(offers_data)
        for data in offers_data['data']:
            new_offer = {
                "username": username,
                "last_seen": user_data_last_seen,
                "ad_name": data['paymentMethodName'],
                "amount": data['fiatPricePerCrypto'],
                "total_trades": user_data_trades_count,
                "currency_code": data['fiatCurrencyCode'],
            }
            total_offers_data.append(new_offer)

    response = make_response(total_offers_data)

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.status_code = 200
    response.mimetype = 'application/json'
    return response


# Call to run the app if the current file is directly executed
if __name__ == "__main__":
    app.run(debug=True)
