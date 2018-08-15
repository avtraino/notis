import requests, json, time
import secrets
from notify import send_email

def genworth():
    api = 'https://maps.googleapis.com/maps/api/directions/json?'
    nodes = 'origin=Park+and+Tilden+Richmond+VA&destination=Genworth+Richmond'
    depart = "&departure_time=now"
    alts = "&alternatives=true"
    key = '&key='+ secrets.maps_key
    link = api+nodes+depart+alts+key
    # print(link)
    res = requests.get(link)
    routes = res.json()['routes']
    tups = []
    for r in routes:
        t = (r['legs'][0]['duration']['value'],r['summary'])
        tups.append(t)
    if min(tups)[1] != "I-64":
        return "Genworth Traffic: Check I-64"
    else:
        return None

# stamp = time.strftime('%Y-%m-%d')

if __name__ == "__main__":
    traffic = genworth()
    if traffic:
        send_email(traffic)