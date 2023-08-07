from werkzeug.local import Local
import sqlite3


local = Local()

def get_db():
    """ 
    get db

    Parameters
    ----------

    Returns
    -------
    .db

    """
    if not hasattr(local, "db"):
        local.db = sqlite3.connect("database.db")
    return local.db

def get_cursor():
    """ 
    Create user table

    """
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
