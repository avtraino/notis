import httpx, json, sqlite3
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
    1. Get Al's recipes json 
    2. Check recipes against database
    3. If changed recipes, then notify and move changes to database
    """

    subject = "Site diff: Al's recipes"
    body = "<h1>New recipes from alvannatta.com</h1><br>"
    send_trigger = False

    cursor = conn.cursor()

    # get existing recipes from sqlite
    db_recipes_table = cursor.execute("SELECT * FROM SITE_DIFF_recipes").fetchall()
    db_recipes = db_recipes_table
    
    # get current recipes from alvannatta.com 
    site_recipes = []
    res = httpx.get('https://alvannatta.com/api/recipes')
    json = res.json()

    for recipe in json:
        if recipe['private'] == 1:
            continue
        recipe_dict = {"recipe_num" : recipe['recipe_num'], "recipe_name" : recipe['recipe_name'], "recipe_href" : recipe['recipe_href'], "image_src" : recipe['image_src']}
        site_recipes.append(recipe_dict)

    add_recipes = []
    for site_recipe in site_recipes:
        if site_recipe['recipe_num'] not in [x['recipe_num'] for x in db_recipes]:
            send_trigger = True
            body = body + f"""<h2>{site_recipe['recipe_name']} <a href="https://alvannatta.com/recipes/{site_recipe['recipe_href']}">(link)</a> </h2> <img src="https://alvannatta.com/recipe-images/{site_recipe['image_src']}" width="500" height="600">  <br><br>"""
            add_recipes.append((site_recipe['recipe_num'], site_recipe['recipe_name']))

    remove_recipes = []
    for db_recipe in db_recipes:
        if db_recipe['recipe_num'] not in [x['recipe_num'] for x in site_recipes]:
            send_trigger = True
            body = body + f"Removed: {db_recipe['recipe_name']} \n"
            remove_recipes.append((db_recipe['recipe_num'],))

    cursor.executemany("INSERT INTO SITE_DIFF_recipes (recipe_num, recipe_name, date_added) VALUES (?, ?, datetime('now', 'localtime'))", add_recipes)
    cursor.executemany("DELETE FROM SITE_DIFF_recipes WHERE recipe_num = (?) ", remove_recipes)

    if send_trigger == True:
        send_email(subject, body, send_to=secrets.site_diff_to, content_type="text/html")  
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