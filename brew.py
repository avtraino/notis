import httpx, json, sqlite3
import logging, os
import secrets
from notify import send_email


logging.basicConfig(filename=secrets.logfile, level=logging.INFO, 
format="%(asctime)s - BREW - %(levelname)s - %(message)s", 
datefmt="%Y-%m-%d %H:%M:%S")

abspath = os.path.abspath(__file__)
proj_dir = os.path.dirname(abspath)
os.chdir(proj_dir)

conn = sqlite3.connect('data/notis.db')
conn.row_factory = sqlite3.Row

def top_rated():
    """
    1. Get beer list from database 
    2. Get list of new checkins from friends
    3. If checkin rating is high and beer isn't on beer list already, then notify and add to beer list
    """

    subject = "Untappd Gems"
    body = "Here are the new beers your friends are excited about:\n"
    send_ready = False

    cursor = conn.cursor()

    old_recent = cursor.execute("SELECT value FROM BREW_app_data WHERE parameter = 'recent_checkin'").fetchone()[0]

    # get new checkins
    endpoint = f'https://api.untappd.com/v4/checkin/recent?limit=50&min_id={old_recent}&access_token={secrets.untappd_token}'
    res = httpx.get(endpoint)
    block = res.json()

    # if new checkins, process
    if block['response']['checkins']['count'] > 0:

        new_recent = str(block['response']['checkins']['items'][0]['checkin_id'])
        checkins = block['response']['checkins']['items']
        new_beer_list = []

        current_beer_list = cursor.execute("SELECT * FROM BREW_top_rated")
        current_bids = [row['beer_id'] for row in current_beer_list]

        for i in checkins:
            name = f"{i['user']['first_name']} {i['user']['last_name']}"
            beer = i['beer']['beer_name']
            bid = i['beer']['bid']
            brewery = i['brewery']['brewery_name']
            rating = i['rating_score']
            if name not in secrets.bad_taste:
                if rating >= 4.5:
                    new_beer = {"bid":bid, "name":beer, "brewery":brewery}
                    if new_beer['bid'] not in current_bids:
                        add = f"\n - {name} gave {str(rating)} stars to {beer} by {brewery}"
                        body = body + add
                        new_beer_list.append((new_beer['bid'], new_beer['name'], new_beer['brewery']))
                        current_bids.append(new_beer['bid'])
                        send_ready = True
        
        if send_ready == True:
            send_email(subject, body)  
            logging.info("Beers email sent. New recent: " + new_recent)
        else:
            logging.info("New checkins. Nothing premium.")
        
        cursor.executemany("INSERT INTO BREW_top_rated (beer_id, beer_name, brewery) VALUES (?,?,?)", new_beer_list)
        cursor.execute("UPDATE BREW_app_data SET value=? WHERE parameter == 'recent_checkin'", (new_recent,))
    else:
        logging.info("No new checkins")

    conn.commit()
    conn.close()    


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