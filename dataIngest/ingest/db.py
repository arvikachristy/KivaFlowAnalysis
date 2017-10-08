""" This is the database 'adapter'.

This is where we would put the abstraction for the database. Exactly what goes in here is a complicated topic but the goal is to be able to swap databases without changing anything in your app but this file

"""

import psycopg2

def insert(data):
    for row in data:
        with Cursor() as cur:
            cur.execute("""
                INSERT INTO data ("kiva_id", "lender_name", "is_important_lender")
                VALUES (%s, %s, %s)
            """, tuple(row.values()))


def setup():
    with Cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS data (
                id serial PRIMARY KEY,
                kiva_id integer, 
                lender_name varchar,
                is_important_lender boolean
            );
        """)


class Cursor():
    def __init__(self):
        self._conn = None
        self._cur = None

    def __enter__(self):
        self._conn = psycopg2.connect(user='postgres', dbname='postgres', host='postgres')
        self._cur = self._conn.cursor()
        return self._cur

    def __exit__(self, *args):
        self._conn.commit()
        self._cur.close()
        self._conn.close()

