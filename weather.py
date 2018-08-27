import requests, json
import logging
import secrets
from notify import send_email

logging.basicConfig(filename=secrets.logfile, level=logging.DEBUG, 
                    format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

def heavy_rain():
    key = secrets.dark_key
    lat, lon = '37.562', '-77.479'
    options = '?units=si&exclude=hourly,minutely'
    link = "https://api.darksky.net/forecast/"+key+lat+","+lon+options
    # print(link)
    res = requests.get(link)
    block = res.json()
    pim = block['daily']['data'][0]['precipIntensityMax']
    summ = block['daily']['data'][0]['summary']
    if pim > 5:
        sub = "Weather Alert: Possible heavy rain today"
        body = "Forecast: " + summ
        send_email(sub, body)
        print("Weather notis sent")
        logging.info("Email sent: YES")
    else:
        print("weather is fine")
        logging.info("Email sent: NO")

def main():
    try:
        heavy_rain()
    except:
        logging.exception("heavy_rain() function did not run properly")

if __name__ == "__main__":
    main()
    