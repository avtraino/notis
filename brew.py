import requests, json
import logging
import secrets
from notify import send_email

logging.basicConfig(filename=secrets.logfile, level=logging.INFO, 
                    format="%(asctime)s - BREW - %(levelname)s - %(message)s", 
                    datefmt="%Y-%m-%d %H:%M:%S")

def top_rated():
    datafile = 'brew_data/top_rated.json'
    with open(datafile, 'r') as brew:
        data = json.load(brew)
        print("Old Data: ", data)
        recent = data['recent']

    key = secrets.untappd_token
    endpoint = 'https://api.untappd.com/v4/checkin/recent?limit=50&min_id='+recent+'&access_token='
    link = endpoint + key 
    print(link)
    res = requests.get(link)
    output = res.text
    print(output)
    block = res.json()
    if block['response']['checkins']['count'] > 0:

        try:
            new_recent = block['response']['checkins']['items'][0]['checkin_id']
            data['recent'] = str(new_recent)
        except IndexError:
            pass
            
        # data['beer_list'].append(add_beer)

        with open(datafile, 'w') as brew:
            json.dump(data, brew)

        print("New Data: ", data)
    else:
        logging.info("no new checkins")

def main():
    try:
        top_rated()
    except:
        logging.exception("top_rated() function did not run properly")
    

if __name__ == "__main__":

    main()
    # debug()