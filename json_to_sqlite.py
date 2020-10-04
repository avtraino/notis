import sqlite3, json, httpx
import secrets

conn = sqlite3.connect('data/notis.db')
conn.row_factory = sqlite3.Row


def migrate_from_json():
    datafile = 'data/top_rated.json'
    with open(datafile, 'r') as brew:
        data = json.load(brew)
        recent = data['recent']
        beer_list = data['beer_list']

    cursor = conn.cursor()

    beers = []
    for beer in beer_list:
        beers.append((beer['bid'], beer['name']))

    cursor.executemany('INSERT OR IGNORE INTO BREW_top_rated VALUES (?,?, null)', beers)
    conn.commit()


def update_breweries():
    cursor = conn.cursor()
    cursor.execute("SELECT beer_id FROM BREW_top_rated where brewery is null")
    beers = [row['beer_id'] for row in cursor.fetchall()]
    for beer in beers:
        bid = beer
        endpoint = f'https://api.untappd.com/v4/beer/info/{bid}?access_token={secrets.untappd_token}'
        res = httpx.get(endpoint)
        block = res.json()
        brewery = block['response']['beer']['brewery']['brewery_name']
        print(bid, brewery)
        cursor.execute("UPDATE BREW_top_rated SET brewery=? WHERE beer_id=?", (brewery, bid))
        conn.commit()


migrate_from_json()
update_breweries()


conn.close()