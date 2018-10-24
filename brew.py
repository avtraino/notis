import requests, json
import logging, os
import secrets
from notify import send_email

logging.basicConfig(filename=secrets.logfile, level=logging.INFO, 
                    format="%(asctime)s - BREW - %(levelname)s - %(message)s", 
                    datefmt="%Y-%m-%d %H:%M:%S")

abspath = os.path.abspath(__file__)
proj_dir = os.path.dirname(abspath)
os.chdir(proj_dir)

def top_rated():
    """
    1. Get list of recent beers I've had, add new ones to beer list in JSON 
    2. Get list of new checkins from friends
    3. If checkin rating is high and beer isn't on beer list already, then notify and add to beer list
    """

    subject = "Untappd Gems"
    body = "Here are the new beers your friends are excited about:\n"
    send_ready = False

    # open data file
    datafile = 'data/top_rated.json'
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
            if name not in secrets.bad_taste:
                if rating >= 4.5:
                    new_beer = {"bid":bid, "name":beer}
                    if new_beer['bid'] not in current_bids:
                        add = "\n - " + name + " gave " + str(rating) + " stars to the "  + beer + " by " + brewery
                        body = body + add
                        beer_list.append(new_beer)
                        send_ready = True
        
        if send_ready == True:
            send_email(subject, body)  
            logging.info("Beers email sent. New recent: " + data['recent'])
        else:
            logging.info("New checkins. Nothing premium.")
        
    else:
        logging.info("No new checkins")

    # write new data 
    with open(datafile, 'w') as brew:
        json.dump(data, brew)


def main():
    try:
        top_rated()
    except:
        logging.exception("top_rated() function did not run properly")
        send_email("Notis logs: top_rated() didn't run properly")
    
def debug():
    pass

if __name__ == "__main__":

    main()
    # debug()