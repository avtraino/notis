import requests, json, time
import secrets
from notify import send_email

def genworth():
    api = 'https://maps.googleapis.com/maps/api/directions/json?'
    nodes = 'origin=Park+and+Tilden+Richmond+VA&destination=Genworth+Richmond'
    options = "&departure_time=now&alternatives=true"
    key = '&key='+ secrets.maps_key
    link = api+nodes+options+key
    # print(link)
    res = requests.get(link)
    routes = res.json()['routes']
    tups = []
    for r in routes:
        t = (r['legs'][0]['duration']['value'],r['summary'])
        tups.append(t)
    if min(tups)[1] != "I-64":
        sub = "Traffic Alert: Genworth"
        body = "I-64 is not fastest route"
        send_email(sub, body)
    else:
        pass

def main():
    # stamp = time.strftime('%Y-%m-%d')
    genworth()

if __name__ == "__main__":
    main()