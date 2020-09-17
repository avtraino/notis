import httpx, json
import logging
import secrets
from notify import send_email

logging.basicConfig(filename=secrets.logfile, level=logging.INFO, 
                    format="%(asctime)s - TRAFFIC - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

def commute():
    api = 'https://maps.googleapis.com/maps/api/directions/json?'
    nodes = 'origin='+secrets.point_a + '&' + 'destination='+secrets.point_b
    options = "&departure_time=now&alternatives=true"
    key = '&key='+ secrets.maps_key
    link = api+nodes+options+key

    res = httpx.get(link)
    routes = res.json()['routes']
    tups = []

    # make tuples out of routes, Tuple(duration, steps)
    for r in routes:
        duration = r['legs'][0]['duration_in_traffic']['value']
        steps = []
        for step in r['legs'][0]['steps']:
            steps.append(step['html_instructions'])
        tup = (duration, steps)
        tups.append(tup)
        
    best_route = min(tups)[1]
    traffic = not all(any(string in step for step in best_route) for string in ['I-195 N', '183B'])

    if traffic:
        subject = "Traffic Alert"
        body = "I-64 is not the fastest route"
        send_email(subject, body)
        logging.info("Trigger email: YES")
    else:
        logging.info("Trigger email: NO")
        
def main():
    try:
        commute()
    except:
        logging.exception("commute() function did not run properly")
        send_email("Notis logs: traffic_morning.py didn't run properly")

if __name__ == "__main__":
    main()