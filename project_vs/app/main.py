import re
import bcrypt

from app.database import get_db, get_cursor

    
class UserController:

    @staticmethod
    def hash_password(password : str) -> bytes:
        """
        Hash password

        Parameters
        ----------
        password : str

        Returns
        -------
        bytes

        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

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
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
            
    def is_user_valid(self, user_name : str) -> tuple:
        """
        Is user valid

        Parameters
        ----------
        user_name : str

        Returns
        -------
        tuple

        """
        cursor = get_cursor()
        cursor.execute(
            "SELECT password FROM USER WHERE username = ?", (user_name,)
        )
        return cursor.fetchone()   

    def insert_user(self, user_data: dict):
        """
        Insert user

        Parameters
        ----------
        user_data: dict

        """
        error_message = None

        if not self.is_valid_email(user_data["mail"]):
            error_message = "Invalid email address. Please enter a valid email."

        if not self.is_valid_password(user_data["password"]):
            error_message = (
                    "Length: At least 8 characters\
                    Both lowercase and uppercase letters\
                    At least one digit"
            ) 

        if user_data["password"] != user_data["password2"]:
            error_message = "The passwords do not match. Please try again."

        if not (hashed_password := self.hash_password(user_data["password"])):
            error_message = "Username alredy exists. Replace your username"
        
        if any(value.strip() == "" for value in user_data.values()):
            error_message = "Fields cannot be empty or contain only whitespace"
        
        if error_message:
            return error_message

        with get_db() as con:
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO USER( \
                    name, surname, mail, username, password \
                )\
                VALUES(?, ?, ?, ?, ?)", (  
                    user_data["name"], 
                    user_data["surname"],
                    user_data["mail"], 
                    user_data["username"],
                    hashed_password
                )
            )
            con.commit()

    def is_valid_email(self, mail_address: str) -> bool:
        """
        Is valid email

        Parameters
        ----------
        mail_address : str

        Returns
        -------
        bool

        """
        return re.match(r'^[\w\.-]+@[\w\.-]+$', mail_address)

    def is_valid_password(self, password: str) -> bool:   
        """
        Is valid email

        Parameters
        ----------
        password : str

        Returns
        -------
        bool

        """
        return len(password) >= 8 and \
                        any(char.islower() for char in password) and \
                        any(char.isupper() for char in password) and \
                        any(char.isdigit() for char in password)
        
         
    

class BookingController:
    
    def is_booking_duplicate(self, booking_data: dict) -> tuple:
        """
        Is booking duplicate

        Parameters
        ----------
        booking_data: dict

        Returns
        -------
        tuple

        """
        with get_db() as con:
            cursor = con.cursor()
            cursor.execute("SELECT id FROM BOOKING_TABLE WHERE date = ? \
                            AND time = ?", (
                                    booking_data.form['date'], 
                                    booking_data.form["time"]
                            )
            )
            return cursor.fetchone()    
            
    def insert_booking(self, booking_data: dict):
        """
        Insert booking

        Parameters
        ----------
        booking_data : dict

        """
        with get_db() as con: 
            cursor = con.cursor()
            cursor.execute(
                    "INSERT INTO BOOKING_TABLE(date, time, count, booked)\
                    VALUES(?, ?, ?, ?)", (
                        booking_data["date"],
                        booking_data["time"], 
                        booking_data["guests"],
                        booking_data["booked"]
                    )
            )
            con.commit()