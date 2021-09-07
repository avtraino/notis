from datetime import datetime, timedelta, timezone
import httpx, json
import logging, traceback
import secrets
from notify import send_email

logging.basicConfig(filename=secrets.logpath+'weather.log', level=logging.INFO, 
                    format="%(asctime)s - WEATHER - %(levelname)s - %(message)s", 
                    datefmt="%Y-%m-%d %H:%M:%S")

next_nine_hours = ( datetime.utcnow() + timedelta(hours=9) ).strftime('%Y-%m-%dT%H:%M:%SZ')
bad_codes = {4201: "Heavy Rain", 5101: "Heavy Snow", 6000: "Freezing Drizzle", 6001: "Freezing Rain", 6201: "Heavy Freezing Rain", 8000: "Thunderstorm"}
    
def heavy_rain():
    url = "https://api.tomorrow.io/v4/timelines"
    querystring = {   # defaults: unit_system = si
        "location" : '37.557 ,-77.475', 
        "endTime" : next_nine_hours, 
        "fields" : "precipitationIntensity,precipitationProbability,weatherCode",
        "apikey" : secrets.tomorrow_key}

    res = httpx.get(url, params=querystring)
    block = res.json()

    bad_hours, bad_hour_count = "", 0
    for hour in block['data']['timelines'][0]['intervals']:
        utc_string = hour['startTime']
        probability = hour['values']['precipitationProbability']
        code = hour['values']['weatherCode']
        precip = round(hour['values']['precipitationIntensity'],1)
        if (probability >= 25) and (code in bad_codes.keys()):
            weather_str = bad_codes[code]
            local_stamp = datetime.strptime(utc_string, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc).astimezone(tz=None)
            nice_time = local_stamp.strftime("%I%p")
            bad_hour_count = bad_hour_count + 1
            bad_hours = bad_hours + f"{nice_time} -- {weather_str} -- {precip} mm/hr -- {probability}% chance \n"

            
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
        tb = traceback.format_exc()
        logging.exception("heavy_rain() function did not run properly")
        send_email("Notis logs: weather.py didn't run properly", tb)

if __name__ == "__main__":
    main()

