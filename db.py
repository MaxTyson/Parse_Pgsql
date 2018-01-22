import psycopg2
from config import DB, DATA

conn = psycopg2.connect("dbname={} user={} host={} password={}".format(DB['db_name'],
                                                                       DB['user_name'],
                                                                       DB['host'],
                                                                       DB['pas'])
)
cur = conn.cursor()


def insert_category(name, url):
    # Inserts new category to category table
    return """ INSERT INTO category (name, url)
        VALUES ('{}', '{}'); """.format(name, url)


def add_category_table():
    # Fills categories table by data
    for category in DATA['categories']:
        cur.execute(insert_category(category, DATA['ids_url'].format(category)))

    return conn.commit()


def get_category_id(category_name):
    # Takes category name and returns his id
    cur.execute(""" SELECT id FROM category
        WHERE category.name='{}' """.format(category_name))

    return cur.fetchall()[0][0]                                 # if duplicated - returns only one id

# add_category_table()    # call one time to fill table "category"

def insert_item(category_name, *args):
    # If data doesn't exist in DB - makes INSERT, otherwise make UPDATE
    cur.execute(""" INSERT INTO item (item_id, author, score, time, title, type, url, category_fk_id)
    VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')
    ON CONFLICT (item_id) DO UPDATE SET (author, score, time, title, url) =
    (EXCLUDED.author, EXCLUDED.score, EXCLUDED.time, EXCLUDED.title, EXCLUDED.url);
    """.format(args[0],
               args[1],
               args[2],
               args[3],
               args[4],
               args[5],
               args[6],
               get_category_id(category_name))

    )
    return conn.commit()

# cur.execute(a)
