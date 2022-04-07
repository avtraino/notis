import httpx, json, sqlite3
from bs4 import BeautifulSoup
import logging, os, traceback
import secrets
from notify import send_email


logging.basicConfig(filename=secrets.logpath+'site_diff.log', level=logging.INFO, 
format="%(asctime)s - SITE_DIFF - %(levelname)s - %(message)s", 
datefmt="%Y-%m-%d %H:%M:%S")

abspath = os.path.abspath(__file__)
proj_dir = os.path.dirname(abspath)
os.chdir(proj_dir)

conn = sqlite3.connect('data/notis.db')
conn.row_factory = sqlite3.Row

def alvan_recipes():
    """
    1. Get html for Al's recipes page 
    2. Check recipes against database
    3. If changed recipes, then notify and move changes to database
    """

    subject = "Site diff: Al's recipes"
    body = "Changes to alvannatta.com/recipes:\n"
    send_trigger = False

    cursor = conn.cursor()

    # get existing recipes from sqlite
    db_recipes_table = cursor.execute("SELECT * FROM SITE_DIFF_recipes").fetchall()
    db_recipes = [ row['name'] for row in db_recipes_table ]
    
    # get current recipes from alvannatta.com 
    site_recipes = []
    res = httpx.get('https://www.alvannatta.com/recipes')
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        recipe_name = link.contents[0]
        site_recipes.append(recipe_name)

    add_recipes = []
    for site_recipe in site_recipes:
        if site_recipe not in db_recipes:
            send_trigger = True
            body = body + f"Added: {site_recipe} \n"
            add_recipes.append((site_recipe,))

    remove_recipes = []
    for db_recipe in db_recipes:
        if db_recipe not in site_recipes:
            send_trigger = True
            body = body + f"Removed: {db_recipe} \n"
            remove_recipes.append((db_recipe,))

    cursor.executemany("INSERT INTO SITE_DIFF_recipes (name, date_added) VALUES (?, datetime('now', 'localtime'))", add_recipes)
    cursor.executemany("DELETE FROM SITE_DIFF_recipes WHERE name = (?) ", remove_recipes)

    if send_trigger == True:
        send_email(subject, body, secrets.site_diff_to)  
        logging.info("alvan_recipes() - recipes updated, sending email")        
    else:
        logging.info("alvan_recipes() - no recipe changes")

    conn.commit()
    conn.close()    


def main():
    try:
        alvan_recipes()
    except httpx.ConnectError: 
        logging.error("httpx could not connect to alvannatta.com")
    except httpx.ConnectTimeout: 
        logging.error("httpx timeout reached trying alvannatta.com")
    except:
        tb = traceback.format_exc()
        logging.exception("alvan_recipes() function did not run properly")
        send_email("Notis logs: site_diff didn't run properly", tb)
    
def debug():
    pass

if __name__ == "__main__":

    main()
    # debug()