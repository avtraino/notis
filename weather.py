from datetime import datetime, timedelta, timezone
import httpx, json
import logging
import secrets
from notify import send_email

logging.basicConfig(filename=secrets.logpath+'weather.log', level=logging.INFO, 
                    format="%(asctime)s - WEATHER - %(levelname)s - %(message)s", 
                    datefmt="%Y-%m-%d %H:%M:%S")

next_nine_hours = ( datetime.utcnow() + timedelta(hours=9) ).strftime('%Y-%m-%dT%H:%M:%SZ')
bad_codes = ["rain_heavy", "snow_heavy", "freezing_rain_heavy", "tstorm"]
    
def heavy_rain():
    url = "https://api.climacell.co/v3/weather/forecast/hourly"
    querystring = {   # defaults: unit_system = si
        "lat" : '37.557', "lon" : '-77.475', 
        "start_time" : "now", "end_time" : next_nine_hours, 
        "fields" : "precipitation,weather_code,precipitation_probability",
        "apikey" : secrets.clima_key}

    res = httpx.get(url, params=querystring)
    block = res.json()

    bad_hours, bad_hour_count = "", 0
    for hour in block:
        utc_string = hour['observation_time']['value']
        probability = hour['precipitation_probability']['value']
        code = hour['weather_code']['value']
        precip = round(hour['precipitation']['value'],1)
        print(f"nice_time: {nice_time} -- code: {code} -- precip: {precip} mm/hr -- prob: {probability}% chance")
        if (probability >= 25) and (code in bad_codes): 
            local_stamp = datetime.strptime(utc_string, '%Y-%m-%dT%H:%M:%S.000Z').replace(tzinfo=timezone.utc).astimezone(tz=None)
            nice_time = local_stamp.strftime("%I%p")
            bad_hour_count = bad_hour_count + 1
            bad_hours = bad_hours + f"{nice_time} -- {code} -- {precip} mm/hr -- {probability}% chance \n"


    if bad_hour_count > 0:
        subject = f"Weather Alert: {bad_hour_count} hours with heavy precipitation"
        body = bad_hours
        send_email(subject, body)
        logging.info("Trigger email: YES")
    else:
        logging.info("Trigger email: NO")

def main():
    try:
        heavy_rain()
    except:
        logging.exception("heavy_rain() function did not run properly")
        send_email("Notis logs: weather.py didn't run properly")

if __name__ == "__main__":
    main()
    
