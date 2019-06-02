import requests, json
import logging
import secrets
from notify import send_email

logging.basicConfig(filename=secrets.logfile, level=logging.INFO, 
                    format="%(asctime)s - WEATHER - %(levelname)s - %(message)s", 
                    datefmt="%Y-%m-%d %H:%M:%S")

def heavy_rain():
    key = secrets.dark_key
    lat, lon = '37.562', '-77.479'
    options = '?units=si&exclude=hourly,minutely'
    link = "https://api.darksky.net/forecast/"+key+"/"+lat+","+lon+options

    res = requests.get(link)
    block = res.json()
    pim = block['daily']['data'][0]['precipIntensityMax']
    summ = block['daily']['data'][0]['summary']

    if pim > 3:
        subject = "Weather Alert: Heavy rain today"
        body = "Forecast: " + summ
        send_email(subject, body)
        logging.info("Trigger email: YES")
    else:
        logging.info("Trigger email: NO")

def main():
    try:
        heavy_rain()
    except:
        logging.exception("heavy_rain() function did not run properly")
        send_email("Notis logs: weather() didn't run properly")

if __name__ == "__main__":
    main()
    
