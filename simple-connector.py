"""Make a request to google every 5 seconds and store the status code in a file."""
import time
import requests

# run infinitely
while (1 is 1):
    r = requests.get('http://google.com')
    with open('myfile.txt', 'a+') as file:
        file.write(str(r.status_code))
    time.sleep(5)
