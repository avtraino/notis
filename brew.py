import requests, json
import logging
import secrets
from notify import send_email

logging.basicConfig(filename=secrets.logfile, level=logging.INFO, 
                    format="%(asctime)s - BREW - %(levelname)s - %(message)s", 
                    datefmt="%Y-%m-%d %H:%M:%S")

def top_rated():
    """
    1. Get list of recent beers I've had, add new ones to beer list in JSON 
    2. Get list of new checkins from friends
    3. If checkin rating is high and beer isn't on beer list already, then notify and add to beer list
    """

    # open data file
    datafile = 'brew_data/top_rated.json'
    with open(datafile, 'r') as brew:
        data = json.load(brew)
        recent = data['recent']
        beer_list = data['beer_list']
    
    # get new checkins
    key = secrets.untappd_token
    endpoint = 'https://api.untappd.com/v4/checkin/recent?limit=50&min_id='+recent+'&access_token='
    link = endpoint + key 
    res = requests.get(link)
    block = res.json()

    # if new checkins, process
    if block['response']['checkins']['count'] > 0:

        new_recent = block['response']['checkins']['items'][0]['checkin_id']
        data['recent'] = str(new_recent)
        
        current_bids = [i['bid'] for i in beer_list]
        checkins = block['response']['checkins']['items']

        for i in checkins:
            name = i['user']['first_name'] + " " + i['user']['last_name']
            beer = i['beer']['beer_name']
            bid = str(i['beer']['bid'])
            brewery = i['brewery']['brewery_name']
            rating = i['rating_score']
            if rating >= 4.5:
                new_beer = {"bid":bid, "name":beer}
                if new_beer['bid'] not in current_bids:
                    print(name , "gave the", beer , "by" , brewery , str(rating) , "stars")
                    beer_list.append(new_beer)
            
        logging.info("Beers logged. New recent: " + data['recent'])
    else:
        logging.info("no new checkins")

    # write new data 
    with open(datafile, 'w') as brew:
        json.dump(data, brew)


def main():
    try:
        top_rated()
    except:
        logging.exception("top_rated() function did not run properly")
    
def debug():
    pass

if __name__ == "__main__":

    main()
    # debug()