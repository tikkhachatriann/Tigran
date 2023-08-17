import re
import bcrypt

from app.database import get_db, get_cursor

    
class UserControler:

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

    def insert_user(self, name: str, sur_name: str, mail_address: str,
                    user_name: str, hashed_password: bytes):
        """
        Insert user

        Parameters
        ----------
        name : str
        sur_name: str
        mail_address: str
        user_name: str
        hashed_password: bytes

        """
        with get_db() as con:
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO USER( \
                    name, surname, mail, username, password \
                )  \
                VALUES(?, ?, ?, ?, ?)", (  
                    name, sur_name, mail_address, 
                    user_name, hashed_password
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
        password_check= len(password) >= 8 and \
                        any(char.islower() for char in password) and \
                        any(char.isupper() for char in password) and \
                        any(char.isdigit() for char in password)
        
        return password_check

    def validate_registration(
        self,
        mail_address: str,
        password: str, 
        password2: str
    ) ->str:
        """
        Validate registration

        Parameters
        ----------
        mail_address: str 
        password : str
        password2: str
        
        Returns
        -------
        bool

        """
        error_message = None

        if not self.is_valid_email(mail_address):
            error_message = "Invalid email address. Please enter a valid email."

        if not self.is_valid_password(password):
            error_message = (
                "Password must be at least 8 characters long. "
                "Password must include both lowercase and uppercase letters. "
                "Password must include at least one digit."
            ) 

        if password != password2:
            error_message = "The passwords do not match. Please try again."

        return error_message
    

class BookingControler:
    
    def is_booking_duplicate(self, date: str, time: str) -> tuple:
        """
        Is booking duplicate

        Parameters
        ----------
        date : str
        time : str

        Returns
        -------
        tuple

        """
        with get_db() as con:
            cursor = con.cursor()
            cursor.execute("SELECT id FROM BOOKING_TABLE WHERE date = ? \
                            AND time = ?", (date, time))
            return cursor.fetchone()    
            
    def insert_booking(self, date: str, time: str, guests: int, booked: bool):
        """
        Insert booking

        Parameters
        ----------
        date : str
        time : str
        guests : int
        booked : bool

        """
        with get_db() as con: 
            cursor = con.cursor()
            cursor.execute(
                    "INSERT INTO BOOKING_TABLE(date, time, count, booked)\
                    VALUES(?, ?, ?, ?)", (date, time, guests, booked)
            )
            con.commit()