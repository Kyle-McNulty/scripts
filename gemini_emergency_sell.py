import requests
import base64
import hmac
import json
import hashlib
import time
from hashlib import sha384

price_url = "https://api.gemini.com/v1/pubticker/btcusd"
sell_url = "https://api.gemini.com/v1/order/new"
cancel_url = "https://api.gemini.com/v1/order/cancel/all"

# file on the local machine containing secret key and bitcoin amount
secret_file = open('gemini_secret.txt', 'r')
gemini_api_key = secret_file.readline().strip()
gemini_api_secret = secret_file.readline().strip()
btc_amount = secret_file.readline().strip()
sell_point = secret_file.readline().strip()

nonce = int(round(time.time() * 1000))

json_payload = {
    "request": "/v1/order/new",
    "nonce": nonce,
    "client_order_id": "20150102-4738720", 
    "symbol": "btcusd",      
    "amount": btc_amount,
    "price": sell_point,
    "side": "sell",            
    "type": "exchange limit" 
}

# monitor bitcoin prices and sell when it drops below my sell_point
# sell_point is an arbitrary number that I consider a sign of a crash
# based on market values when writing this
loss_index = .95
# this is the default value I am setting for previous since it is
# my break point
previous_ask = sell_point
prev_failed = False
# run infinitely
while 1==1:
    r = requests.get(price_url)
    price_info = json.loads(r.text)
    ask_num = float(price_info['ask'])
    if prev_failed:
        # previous over current gives me the ratio drop in the last second
        # since I made my previous sell request
        loss_index = previous_ask / ask_num
        # post limit for 90% of 
        # the previous ask value over the current ask value * the current ask value
        loss_index *= .9
    # sell_point is the value I want my sell code to start running
    if ask_num < int(sell_point):
        # update nonce
        nonce = int(round(time.time() * 1000))
        json_payload['price'] = str("%.2f" % ((ask_num) * loss_index))
        json_payload['nonce'] = str(nonce)
        b64 = base64.b64encode(json.dumps(json_payload))
        signature = hmac.new(gemini_api_secret, b64, hashlib.sha384).hexdigest()
        headers = {
            'Content-Type': "text/plain",
            'Content-Length': "0",
            'X-GEMINI-APIKEY': gemini_api_key,
            'X-GEMINI-PAYLOAD': b64,
            'X-GEMINI-SIGNATURE': signature,
            'Cache-Control': "no-cache"
        }
        response = requests.request("POST", sell_url, headers=headers)
        print(response.text)
        # increment the nonce for the next request
        # update the previous ask to manage percentage drop
        previous_ask = ask_num

        # after making the sale post, wait a second, 
        # if it hasn't sold, reduce price more
        # this is aggressive so I do not get caught 
        # out in the case of an extreme crash
        time.sleep(1)
        nonce = int(round(time.time() * 1000))
        cancel_payload = {
            "request": "/v1/order/cancel/all",
            "nonce": str(nonce),
        }
        cancel_b64 = base64.b64encode(json.dumps(cancel_payload))
        cancel_signature = hmac.new(gemini_api_secret, cancel_b64, hashlib.sha384).hexdigest()
        cancel_headers = {
            'Content-Type': "text/plain",
            'Content-Length': "0",
            'X-GEMINI-APIKEY': gemini_api_key,
            'X-GEMINI-PAYLOAD': cancel_b64,
            'X-GEMINI-SIGNATURE': cancel_signature,
            'Cache-Control': "no-cache"
        }
        cancel = requests.request("POST", cancel_url, headers=cancel_headers)
        print(cancel.text)
        # if the cancel request goes through, I was unable to sell at the
        # posted value
        prev_failed = True
        # then jump back in to the while loop
    # if the sell wasn't processed, don't wait
    if not prev_failed:
        time.sleep(1)
        # for when I check on the screen process
        print("Still running...\nTime: " + str(time.time()))
