import sqlite3
from werkzeug.local import Local


def get_db():
    local = Local()

    if not hasattr(local, "db"):
        local.db = sqlite3.connect("database.db")
        local.db.row_factory = sqlite3.Row
    return local.db

def get_cursor():
    return get_db().cursor()

def create_user_table():
    with get_db() as con:
        cursor = con.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS USER ( \
                id INTEGER PRIMARY KEY AUTOINCREMENT, \
                name TEXT, surname TEXT, mail TEXT, \
                username TEXT UNIQUE, password TEXT \
            )"
        )

def create_events_table():
    with get_db() as con:
        cursor = con.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS EVENTS ( \
                id INTEGER PRIMARY KEY AUTOINCREMENT\
                week_day TEXT,\
                date TEXT,\
                dj_name TEXT,\
                table_id_list TEXT\
            )"
        )

def create_resereves_table():
    with get_db() as con:
        cursor = con.cursor()
        cursor.execute(
                "CREATE TABLE IF NOT EXISTS RESERVES(\
                    id INTEGER PRIMARY KEY AUTOINCREMENT,\
                    time TEXT,\
                    guests INTEGER\
                )"
        )
