import re
import bcrypt
import bleach
import sqlite3


from app.database import get_db, get_cursor


class UserController:
    
    @staticmethod
    def hash_password(password: str) -> bytes:
        """
        Hash password

        Parameters
        ----------
        password : str

        Returns
        -------
        bytes

        """
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    @staticmethod
    def check_password(password: str, hashed_password: bytes) -> bool:
        """
        Check password

        Parameters
        ----------
        password : str
        hashed_password : bytes

        Returns
        -------
        bool

        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

    @staticmethod
    def is_valid_email(mail_address: str) -> bool:
        """
        Is valid email

        Parameters
        ----------
        mail_address : str

        Returns
        -------
        bool

        """
        return re.match(r"^[\w\.-]+@[\w\.-]+$", mail_address)

    @staticmethod
    def is_valid_password(password: str) -> bool:
        """
        Is valid email

        Parameters
        ----------
        password : str

        Returns
        -------
        bool

        """
        return re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", password)
    
    @staticmethod
    def is_username_exists( username: str) -> tuple:
        """
        Is username exists

        Parameters
        ----------
        username : str

        Returns
        -------
        tuple

        """
        cursor = get_cursor()
        cursor.execute(
            "SELECT username FROM USER WHERE LOWER(username) = LOWER(?)",
            (username,)
        )
        return cursor.fetchone()

    @staticmethod
    def get_user(user_name: str) -> tuple:
        """
        Get user

        Parameters
        ----------
        user_name : str

        Returns
        -------
        tuple

        """
        cursor = get_cursor()
        cursor.execute("SELECT * FROM USER WHERE username = ?", (user_name,))
        return cursor.fetchone()

    def validate_user(self, user_data: dict) -> tuple:
        """
        Validate user

        Parameters
        ----------
        user_data: dict

        Returns
        -------
        tuple

        """
        user_name = user_data["username"]
       
        if user_name == bleach.clean(user_name):
            if user := self.get_user(user_name):
                if self.check_password(user_data["password"], user["password"]):
                    return user

    def register_user(self, user_data: dict):
        """
        Register user

        Parameters
        ----------
        user_data: dict

        """

        if not self.is_valid_email(user_data["mail"]):
            raise ValueError("Invalid email address. Please enter valid email.")

        if not self.is_valid_password(user_data["password"]):
            raise ValueError(
                "Length: At least 8 characters\
                Both lowercase and uppercase letters\
                At least one digit"
            )

        if user_data["password"] != user_data["password2"]:
            raise ValueError("The passwords do not match. Please try again.")

        if self.is_username_exists(user_data["username"]):
            raise ValueError("Username already exists. Replace your username")

        if any(value.strip() == "" for value in user_data.values()):
            raise ValueError("Fields cannot be empty or contains whitespaces")
    
        with get_db() as con:
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO USER(name, surname, mail, username, password)\
                VALUES(?, ?, ?, ?, ?)",
                (
                    user_data["name"],
                    user_data["surname"],
                    user_data["mail"],
                    user_data["username"],
                    self.hash_password(user_data["password"]),
                ),
            )
            con.commit()


class BookingController:
    @staticmethod
    def get_events() -> tuple:
        """
        Get events

        Returns
        -------
        tuple

        """
        cursor = get_cursor()
        cursor.execute("SELECT id, week_day, date, dj_name FROM EVENTS")
        return cursor
    
    @staticmethod
    def get_tables() -> tuple:
        """
        Get tables

        Returns
        -------
        tuple

        """
        cursor = get_cursor()
        cursor.execute("SELECT * FROM RESERVES")
        return cursor

    @staticmethod
    def get_booked_tables(event_id: int) -> list:
        """
        Get booked tables
        
        Parameters
        ----------
        event_id: int

        Returns
        -------
        tuple

        """
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute(
            "SELECT B.table_id FROM RESERVES AS R "\
            "LEFT JOIN BOOKED AS B ON R.id = B.table_id WHERE B.event_id = ?",
            (event_id,)
        )
        result = cursor.fetchall()
        if result:
            booked_list = [item[0] for item in result]
        else:
            booked_list = []
        
        return booked_list
    
    @staticmethod
    def book_table( booking_data: dict):
        """
        Book table

        Parameters
        ----------
        booking_data : dict

        """
        table_id = booking_data["tableId"]
        event_id = booking_data["eventId"]

        with get_db() as con:
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO BOOKED(event_id, table_id)VALUES(?,?)",
                (event_id,table_id)
            )
            con.commit()
