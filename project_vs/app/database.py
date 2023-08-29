from werkzeug.local import Local
import sqlite3


def get_db():
    local = Local()

    if not hasattr(local, "db"):
        local.db = sqlite3.connect("database.db")
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                week_day TEXT, date TEXT, dj_name TEXT \
            )"
        )

def create_resereves_table():
    with get_db() as con:
        cursur = con.cursor()
        cursur.execute(
                "CREATE TABLE IF NOT EXISTS RESERVES(\
                    id INTEGER PRIMARY KEY AUTOINCREMENT,\
                    count INTEGER, booked BOOLEAN\
                )"
        )

def create_booking_table():
    with get_db() as con:
        cursor = con.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS BOOKING_TABLE(\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                count INTEGER, time TEXT \
            )"
        )
    
