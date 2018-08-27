import requests, json
import logging
import secrets
from notify import send_email

logging.basicConfig(filename=secrets.logfile, level=logging.DEBUG, 
                    format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

def genworth():
    key = '&key='+ secrets.maps_key
    api = 'https://maps.googleapis.com/maps/api/directions/json?'
    nodes = 'origin=Park+and+Tilden+Richmond+VA&destination=Genworth+Richmond'
    options = "&departure_time=now&alternatives=true"
    link = api+nodes+options+key
    # print(link)
    res = requests.get(link)
    routes = res.json()['routes']
    tups = []
    for r in routes:
        duration = r['legs'][0]['duration']['value']
        steps = []
        for step in r['legs'][0]['steps']:
            steps.append(step['html_instructions'])
        tup = (duration,steps)
        tups.append(tup)
    best_route = min(tups)[1]
    traffic = not all(any(s in step for step in best_route) for s in ['I-195 N', '183B'])

    if traffic:
        sub = "Traffic Alert: Genworth"
        body = "I-64 is not the fastest route"
        send_email(sub, body)
        print("Traffic notis sent")
        logging.info("Email sent: YES")
    else:
        print("No traffic, 195/64 is best route")
        logging.info("Email sent: NO")
        
def main():
    try:
        genworth()
    except:
        logging.exception("traffic() function did not run properly")

if __name__ == "__main__":
    main()