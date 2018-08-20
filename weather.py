import requests, json, time
from secrets import dark_key
from notify import send_email

def heavy_rain():
    key = dark_key
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
    else:
        pass

def main():
    heavy_rain()

if __name__ == "__main__":
    main()
    